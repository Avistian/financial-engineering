"""Seed scan for lab 010.2: find a market+decoy seed pair satisfying every notebook assertion."""
import numpy as np
import statsmodels.api as sm
from scipy import stats

TRADING_DAYS, N_DAYS, N_NAMES, WIN, H = 252, 2520, 12, 252, 5
SECTOR_OF = np.array([0, 0, 0, 0, 1, 1, 1, 1, 2, 2, 2, 2])

SIG_M, IDIO_LO, IDIO_HI = 0.0105, 0.0090, 0.0140
PHI_S, ETA_S = 0.996, 0.038
PHI_F, GAMMA, DELTA, ETA_F = 0.92, -0.12, 0.06, 0.025
LV_CAP, CLIP_Z, E_ABS_Z = 1.00, 4.0, 0.75
DECOYS = ["mom12m", "value", "quality", "lowvol", "size", "growth",
          "sentiment", "accruals", "carry", "beta_arb", "analyst_rev"]


def std_t(rng, df, size):
    return rng.standard_t(df, size=size) / np.sqrt(df / (df - 2.0))


def simulate(seed, kappa, drift=0.06, burn=800):
    rng = np.random.default_rng(seed)
    n, T = N_NAMES, N_DAYS + burn
    v_lv = ETA_S**2 / (1 - PHI_S**2) + (GAMMA**2 + DELTA**2 * .45 + ETA_F**2) / (1 - PHI_F**2)
    beta = rng.uniform(0.75, 1.35, size=n)
    sec = rng.uniform(0.50, 1.00, size=n)
    idio_bar = rng.uniform(IDIO_LO, IDIO_HI, size=n)
    sm_ = fm_ = 0.0
    si_ = np.zeros(n); fi_ = np.zeros(n)
    R = np.zeros((T, n)); rm = np.zeros(T); rev = np.zeros((T, n))
    alpha = np.zeros(n)
    for t in range(T):
        sig_m = SIG_M * np.exp(min(sm_ + fm_ - v_lv, LV_CAP))
        zm = float(np.clip(std_t(rng, 6, 1)[0], -CLIP_Z, CLIP_Z))
        rm[t] = drift / TRADING_DAYS + sig_m * zm
        f = std_t(rng, 6, 3) * 0.004
        sig_i = idio_bar * np.exp(np.minimum(si_ + fi_ - v_lv, LV_CAP))
        ei = np.clip(std_t(rng, 5, n), -CLIP_Z, CLIP_Z)
        R[t] = beta * rm[t] + sec * f[SECTOR_OF] + sig_i * ei + alpha
        if t >= 4:
            rev[t] = -R[t-4:t+1].sum(0) / (np.sqrt(5.) * idio_bar * 1.9)
        alpha = kappa * (rev[t] - rev[t].mean())
        sm_ = PHI_S * sm_ + ETA_S * rng.normal()
        fm_ = PHI_F * fm_ + GAMMA * zm + DELTA * (abs(zm) - E_ABS_Z) + ETA_F * rng.normal()
        si_ = PHI_S * si_ + ETA_S * rng.normal(size=n)
        fi_ = PHI_F * fi_ + GAMMA * ei + DELTA * (np.abs(ei) - E_ABS_Z) + ETA_F * rng.normal(size=n)
    s = slice(burn, None)
    return R[s], rev[s], rm[s], beta


def zs(a):
    return (a - a.mean(0)) / a.std(0)


def decoys(seed, burn=500):
    rng = np.random.default_rng(seed)
    out = {}
    for nm in DECOYS:
        T = N_DAYS + burn
        c = np.zeros(T); i_ = np.zeros((T, N_NAMES))
        a = rng.uniform(0.6, 2.2)
        for t in range(1, T):
            c[t] = 0.985 * c[t-1] + rng.normal()
            i_[t] = 0.97 * i_[t-1] + rng.normal(size=N_NAMES)
        out[nm] = zs((a * c[:, None] + i_)[burn:])
    return out


def acf(x, lag):
    return float(np.corrcoef(x[:-lag], x[lag:])[0, 1])


def rolling_beta(R):
    mkt = R.mean(1)
    bh = np.full((N_DAYS, N_NAMES), np.nan)
    cs_m = np.concatenate([[0.], np.cumsum(mkt)])
    for t in range(WIN - 1, N_DAYS):
        m = mkt[t-WIN+1:t+1]
        vm = m.var(ddof=1)
        seg = R[t-WIN+1:t+1]
        bh[t] = ((seg - seg.mean(0)) * (m - m.mean())[:, None]).sum(0) / (WIN - 1) / vm
    return bh


def book(sig, R, bh, start=WIN):
    z = sig - sig.mean(1, keepdims=True)
    b = np.nan_to_num(bh, nan=1.0)
    bc = b - b.mean(1, keepdims=True)          # demean beta => neutral on BOTH axes
    z = z - (np.sum(z * bc, 1) / np.sum(bc * bc, 1))[:, None] * bc
    w = z / np.abs(z).sum(1, keepdims=True)
    return (w[start:-1] * R[start+1:]).sum(1), w[start:]


def full_eval(mseed, dseed, kappa, drift):
    R, rev, rm, beta = simulate(mseed, kappa, drift)
    o = {}
    av = R.std(0) * np.sqrt(TRADING_DAYS)
    o["volLo"], o["volHi"] = av.min(), av.max()
    o["idxV"] = R.mean(1).std() * np.sqrt(TRADING_DAYS)
    o["maxR"] = float(np.abs(np.expm1(R)).max())
    o["pxX"] = float(np.exp(R.sum(0)).max())
    o["kurt"] = np.mean([stats.kurtosis(R[:, i]) for i in range(N_NAMES)])
    o["acf1r"] = np.mean([acf(R[:, i], 1) for i in range(N_NAMES)])
    o["acf1a"] = np.mean([acf(np.abs(R[:, i]), 1) for i in range(N_NAMES)])
    o["acf22a"] = np.mean([acf(np.abs(R[:, i]), 22) for i in range(N_NAMES)])
    o["lev"] = np.mean([np.corrcoef(R[:-1, i], np.abs(R[1:, i]))[0, 1] for i in range(N_NAMES)])
    C = np.corrcoef(R.T)
    ev, evec = np.linalg.eigh(C)
    ordr = np.argsort(ev)[::-1]
    ev, evec = ev[ordr], evec[:, ordr]
    o["pc1"] = ev[0] / N_NAMES
    v1 = evec[:, 0] * (1 if evec[:, 0].mean() > 0 else -1)
    o["pc1_pos"] = bool(np.all(v1 > 0))
    o["pc1_gap"] = ev[0] / ev[1]
    s0 = np.expm1(R[:, 0])
    o["corrSL"] = float(np.corrcoef(s0, R[:, 0])[0, 1])
    o["gapdev"] = float(np.abs((s0 - R[:, 0]) - s0**2 / 2).max())
    o["medgap"] = float(np.median(np.abs(s0 - R[:, 0])))

    sigs = {"rev5": zs(rev)}
    sigs.update(decoys(dseed))
    names = list(sigs)
    M = len(names)

    fwd = np.array([R[t+1:t+1+H].sum(0) for t in range(N_DAYS - H)])
    naive = {}
    for s in names:
        f = sm.OLS(fwd.ravel(), sm.add_constant(sigs[s][:N_DAYS-H].ravel())).fit()
        naive[s] = (f.tvalues[1], f.pvalues[1], f.rsquared)
    o["naive_sig"] = sum(1 for s in names if naive[s][1] < 0.05)
    o["naive_decoy_sig"] = sum(1 for s in names if s != "rev5" and naive[s][1] < 0.05)
    o["naive_best_t"] = max(abs(naive[s][0]) for s in names)
    o["naive_maxR2"] = max(naive[s][2] for s in names)

    bh = rolling_beta(R)
    tab = {}
    for s in names:
        p, w = book(sigs[s], R, bh)
        f = sm.OLS(p, np.ones(len(p))).fit()
        tn = f.get_robustcov_results(cov_type="HAC", maxlags=10, use_correction=True).tvalues[0]
        tab[s] = (p.mean()/p.std()*np.sqrt(TRADING_DAYS), tn,
                  float(np.abs(np.diff(w, axis=0)).sum(1).mean()), p)
    o["rank1"] = max(names, key=lambda s: abs(tab[s][1]))
    o["sr"] = tab["rev5"][0]
    o["t_nw"] = tab["rev5"][1]
    o["turn"] = tab["rev5"][2]
    bonf_t = stats.norm.isf(0.05 / (2 * M))
    o["n_uncorr"] = sum(1 for s in names if abs(tab[s][1]) > 1.96)
    o["decoy_max_t"] = max(abs(tab[s][1]) for s in names if s != "rev5")
    o["survives_bonf"] = abs(tab["rev5"][1]) > bonf_t
    o["decoys_dead"] = o["decoy_max_t"] < bonf_t
    pnl = tab["rev5"][3]
    o["bookvol"] = pnl.std() * np.sqrt(TRADING_DAYS)
    o["acf1_pnl"] = acf(pnl, 1)
    fb = sm.OLS(pnl, sm.add_constant(R.mean(1)[WIN+1:])).fit()
    fbh = fb.get_robustcov_results(cov_type="HAC", maxlags=10, use_correction=True)
    o["resid_beta"] = fb.params[1]
    o["resid_beta_t"] = fbh.tvalues[1]
    o["corr_true_mkt"] = float(np.corrcoef(pnl, rm[WIN+1:])[0, 1])
    o["pos_days"] = float((pnl > 0).mean())
    return o


REQ = [
    ("volLo", 0.16, 0.40), ("volHi", 0.18, 0.40), ("idxV", 0.10, 0.30),
    ("maxR", 0.0, 0.16), ("pxX", 1.0, 9.0), ("kurt", 2.2, 10.0),
    ("acf1a", 0.105, 1.0), ("acf22a", 0.021, 1.0), ("lev", -1.0, -0.031),
    ("pc1", 0.30, 0.60), ("pc1_gap", 3.01, 99), ("corrSL", 0.9991, 1.0),
    ("gapdev", 0.0, 0.0029), ("naive_sig", 4, 99), ("naive_decoy_sig", 3, 99),
    ("naive_best_t", 8.01, 99), ("naive_maxR2", 0.0, 0.0199),
    ("sr", 0.95, 1.45), ("t_nw", 3.05, 6.0), ("turn", 0.31, 0.95),
    ("n_uncorr", 2, 99), ("bookvol", 0.02, 0.40),
    ("acf1_pnl", -0.099, 0.099), ("resid_beta", -0.29, 0.29),
    ("corr_true_mkt", -0.119, 0.119), ("pos_days", 0.451, 0.599),
]


def failures(o):
    bad = []
    for k, lo, hi in REQ:
        if not (lo <= o[k] <= hi):
            bad.append(f"{k}={o[k]:.4g}")
    if o["rank1"] != "rev5":
        bad.append(f"rank1={o['rank1']}")
    if not o["survives_bonf"]:
        bad.append("bonf_fail")
    if not o["decoys_dead"]:
        bad.append(f"decoy_t={o['decoy_max_t']:.2f}")
    if not o["pc1_pos"]:
        bad.append("pc1_signs")
    if abs(o["resid_beta_t"]) <= 2:
        bad.append(f"resid_beta_t={o['resid_beta_t']:.2f}")
    return bad


if __name__ == "__main__":
    best = []
    for mseed in range(1, 26):
        for dseed in (23, 31):
            for kappa, drift in ((0.00055, 0.05),):
                try:
                    o = full_eval(mseed, dseed, kappa, drift)
                except Exception as e:
                    print(f"m{mseed} d{dseed}: ERROR {e}")
                    continue
                bad = failures(o)
                tag = "PASS" if not bad else f"{len(bad)} fail"
                print(f"m={mseed:>2} d={dseed} k={kappa} | {tag:>8} | "
                      f"vol {o['volLo']:.2f}-{o['volHi']:.2f} idx {o['idxV']:.2f} "
                      f"maxR {o['maxR']:.3f} px {o['pxX']:.1f} kurt {o['kurt']:.1f} "
                      f"acf1a {o['acf1a']:.3f} acf22 {o['acf22a']:.3f} lev {o['lev']:+.3f} "
                      f"pc1 {o['pc1']:.2f} | naive {o['naive_sig']}/{o['naive_decoy_sig']} "
                      f"t{o['naive_best_t']:.1f} | SR {o['sr']:.2f} tNW {o['t_nw']:.2f} "
                      f"unc {o['n_uncorr']} dmax {o['decoy_max_t']:.2f} "
                      f"rb {o['resid_beta']:+.2f}/{o['resid_beta_t']:+.1f}"
                      + ("" if not bad else "  <- " + ", ".join(bad)))
                if not bad:
                    best.append((mseed, dseed, kappa, drift, o))
    print("\nPASSING:", [(m, d) for m, d, _, _, _ in best])
