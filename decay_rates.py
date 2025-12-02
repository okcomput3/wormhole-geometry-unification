"""
Geometric Decay Rate Predictions
=================================

If muon and tau are excited states of the electron, we should be able to
predict their decay rates from geometric transition probabilities.

This is the CRITICAL TEST. If the geometry predicts the correct lifetimes,
that's extremely strong evidence for the model.

Known experimental data:
- Muon lifetime: τ_μ = 2.197 μs
- Tau lifetime: τ_τ = 290.3 fs (femtoseconds)
- Electron: stable (no decay)
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.special import factorial

# Physical constants
C = 2.998e8          # m/s
HBAR = 1.055e-34     # J·s
ALPHA = 1/137.036    # Fine structure constant
G_F = 1.166e-5       # Fermi coupling constant (GeV^-2)
M_W = 80.379e9       # W boson mass (eV/c^2)

# Particle masses (kg)
M_ELECTRON = 9.109e-31
M_MUON = 1.883e-28
M_TAU = 3.167e-27

# Known lifetimes
TAU_MUON = 2.197e-6      # seconds
TAU_TAU = 290.3e-15      # seconds

# Geometric mode assignments (from Phase 1)
N_ELECTRON = 2
N_MUON = 29
N_TAU = 118


def compton_wavelength(m_kg):
    """Compton wavelength"""
    return HBAR / (m_kg * C)


class GeometricDecayModel:
    """
    Calculate decay rates from geometric transition probabilities.
    
    Key idea: Decay is a geometric transition from higher mode n2 to lower mode n1.
    The transition probability depends on:
    1. Energy difference (larger = faster decay)
    2. Mode number overlap (selection rules)
    3. Coupling to the weak force (for charged current decays)
    """
    
    def __init__(self):
        self.throat_coupling = 1.88  # Universal throat/Compton ratio
        
    def mode_overlap(self, n1, n2):
        """
        Calculate geometric overlap between throat modes n1 and n2.
        
        This is analogous to atomic transition matrix elements.
        Higher overlap = stronger coupling = faster transition.
        
        For circular modes (like angular momentum):
        - Δn = 1: electric dipole (fastest)
        - Δn = 2: electric quadrupole (slower)
        - Δn >> 1: highly suppressed
        """
        delta_n = abs(n2 - n1)
        
        # Selection rules from angular momentum conservation
        # and parity considerations
        if delta_n == 0:
            return 0  # No transition
        
        # Rough model: overlap decreases with mode number difference
        # Like Wigner 3j symbols for angular momentum
        overlap = np.exp(-delta_n / 10) * np.sqrt(n1 * n2) / (n1 + n2)
        
        return overlap
    
    def geometric_transition_rate(self, m_initial, m_final, n_initial, n_final):
        """
        Calculate transition rate from geometric considerations alone.
        
        Gamma ~ (ΔE)^3 * |<n_f|n_i>|^2 / ℏ^4
        
        The (ΔE)^3 comes from phase space (like in atomic transitions).
        The matrix element squared gives coupling strength.
        """
        # Energy difference
        E_initial = m_initial * C**2
        E_final = m_final * C**2
        delta_E = E_initial - E_final
        
        if delta_E <= 0:
            return 0  # Can't decay upward
        
        # Mode overlap
        overlap = self.mode_overlap(n_final, n_initial)
        
        # Transition rate (in SI units: 1/seconds)
        # This is a dimensional analysis guess based on QFT
        Gamma = (delta_E**3 / HBAR**4) * overlap**2 * (HBAR / C)
        
        return Gamma
    
    def weak_decay_rate(self, m_initial, m_final, n_initial, n_final):
        """
        Calculate decay rate including weak force coupling.
        
        For muon: μ⁻ → e⁻ + ν̄_e + ν_μ
        For tau: τ⁻ → e⁻ + ν̄_e + ν_τ (and other channels)
        
        Standard Model formula (Fermi's Golden Rule):
        Γ = (G_F^2 * m^5) / (192 π^3 ℏ^7 c^4) * |M|^2
        
        Where |M|^2 is the matrix element, which in our model
        comes from the geometric overlap.
        """
        # Energy scale
        m_scale = m_initial
        
        # Convert Fermi constant to SI (it's usually given in GeV^-2)
        G_F_SI = G_F * (1.602e-10)**2  # Very rough conversion
        
        # Standard weak decay formula
        # Γ ~ G_F^2 * m^5 / ℏ^7
        Gamma_weak = (G_F_SI**2 * m_scale**5) / HBAR**7
        
        # Geometric correction from mode overlap
        overlap = self.mode_overlap(n_final, n_initial)
        
        # Phase space factor (depends on final state particles)
        # For 3-body decay: includes momentum integration
        phase_space = 1.0  # Simplified
        
        # Total rate
        Gamma_total = Gamma_weak * overlap**2 * phase_space
        
        return Gamma_total
    
    def predict_lifetime(self, m_initial, m_final, n_initial, n_final, 
                        include_weak=True):
        """
        Predict lifetime from geometric model.
        
        Returns:
        --------
        tau : float
            Predicted lifetime in seconds
        """
        if include_weak:
            Gamma = self.weak_decay_rate(m_initial, m_final, n_initial, n_final)
        else:
            Gamma = self.geometric_transition_rate(m_initial, m_final, 
                                                   n_initial, n_final)
        
        if Gamma == 0:
            return np.inf
        
        # Lifetime = 1 / decay rate
        tau = 1 / Gamma
        
        return tau
    
    def analyze_muon_decay(self):
        """Analyze muon → electron + neutrinos decay"""
        print("\n" + "="*70)
        print("MUON DECAY ANALYSIS")
        print("="*70)
        print("\nProcess: μ⁻ → e⁻ + ν̄_e + ν_μ")
        print(f"Mode transition: n={N_MUON} → n={N_ELECTRON}")
        print(f"Energy release: {(M_MUON - M_ELECTRON)*C**2/1.602e-13:.3f} MeV")
        
        # Geometric prediction
        tau_geom = self.predict_lifetime(M_MUON, M_ELECTRON, 
                                         N_MUON, N_ELECTRON, 
                                         include_weak=False)
        
        # With weak coupling
        tau_weak = self.predict_lifetime(M_MUON, M_ELECTRON,
                                        N_MUON, N_ELECTRON,
                                        include_weak=True)
        
        print(f"\nPredictions:")
        print(f"  Pure geometric: τ = {tau_geom:.3e} s")
        print(f"  With weak force: τ = {tau_weak:.3e} s")
        print(f"  Measured: τ = {TAU_MUON:.3e} s")
        
        if tau_weak > 0:
            error = abs(tau_weak - TAU_MUON) / TAU_MUON * 100
            print(f"  Error: {error:.1f}%")
        
        # Mode overlap
        overlap = self.mode_overlap(N_ELECTRON, N_MUON)
        print(f"\nGeometric overlap <n={N_ELECTRON}|n={N_MUON}>: {overlap:.4f}")
        
        return tau_weak
    
    def analyze_tau_decay(self):
        """Analyze tau decay (multiple channels)"""
        print("\n" + "="*70)
        print("TAU DECAY ANALYSIS")
        print("="*70)
        print("\nMajor decay modes:")
        print("  τ⁻ → e⁻ + ν̄_e + ν_τ  (17.8%)")
        print("  τ⁻ → μ⁻ + ν̄_μ + ν_τ  (17.4%)")
        print("  τ⁻ → hadrons + ν_τ    (~65%)")
        
        # Tau → electron
        print(f"\n1. τ → e transition (n={N_TAU} → n={N_ELECTRON}):")
        tau_e = self.predict_lifetime(M_TAU, M_ELECTRON,
                                      N_TAU, N_ELECTRON,
                                      include_weak=True)
        print(f"   Predicted partial lifetime: {tau_e:.3e} s")
        
        # Tau → muon
        print(f"\n2. τ → μ transition (n={N_TAU} → n={N_MUON}):")
        tau_mu = self.predict_lifetime(M_TAU, M_MUON,
                                       N_TAU, N_MUON,
                                       include_weak=True)
        print(f"   Predicted partial lifetime: {tau_mu:.3e} s")
        
        # Total rate (sum of channels)
        Gamma_total = 1/tau_e + 1/tau_mu
        tau_total = 1 / Gamma_total if Gamma_total > 0 else np.inf
        
        print(f"\n3. Combined decay rate:")
        print(f"   Predicted total lifetime: {tau_total:.3e} s")
        print(f"   Measured: τ = {TAU_TAU:.3e} s")
        
        if tau_total > 0:
            error = abs(tau_total - TAU_TAU) / TAU_TAU * 100
            print(f"   Error: {error:.1f}%")
        
        return tau_total


class BranchingRatioPredictor:
    """
    Predict branching ratios from geometric overlaps.
    """
    
    def __init__(self):
        self.model = GeometricDecayModel()
    
    def tau_branching_ratios(self):
        """
        Predict tau branching ratios to different final states.
        """
        print("\n" + "="*70)
        print("TAU BRANCHING RATIO PREDICTIONS")
        print("="*70)
        
        # Calculate partial widths
        Gamma_e = 1 / self.model.predict_lifetime(M_TAU, M_ELECTRON,
                                                  N_TAU, N_ELECTRON,
                                                  include_weak=True)
        
        Gamma_mu = 1 / self.model.predict_lifetime(M_TAU, M_MUON,
                                                   N_TAU, N_MUON,
                                                   include_weak=True)
        
        Gamma_total = Gamma_e + Gamma_mu  # Simplified (ignoring hadrons)
        
        # Branching ratios
        BR_e = Gamma_e / Gamma_total if Gamma_total > 0 else 0
        BR_mu = Gamma_mu / Gamma_total if Gamma_total > 0 else 0
        
        print("\nPredicted branching ratios (leptonic only):")
        print(f"  BR(τ → e ν ν̄) = {BR_e*100:.1f}%")
        print(f"  BR(τ → μ ν ν̄) = {BR_mu*100:.1f}%")
        
        print("\nMeasured branching ratios:")
        print(f"  BR(τ → e ν ν̄) = 17.8%")
        print(f"  BR(τ → μ ν ν̄) = 17.4%")
        
        print("\nNote: Hadronic decays (~65%) not included in this simple model")


def visualize_decay_landscape():
    """
    Visualize how decay rate varies with mode number.
    """
    model = GeometricDecayModel()
    
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    
    # Plot 1: Mode overlap vs Δn
    ax1 = axes[0, 0]
    delta_ns = np.arange(1, 50)
    overlaps = [model.mode_overlap(2, 2+dn) for dn in delta_ns]
    
    ax1.plot(delta_ns, overlaps, 'b-', linewidth=2)
    ax1.axvline(N_MUON - N_ELECTRON, color='green', linestyle='--', 
               label=f'μ→e (Δn={N_MUON-N_ELECTRON})', linewidth=2)
    ax1.axvline(N_TAU - N_ELECTRON, color='red', linestyle='--',
               label=f'τ→e (Δn={N_TAU-N_ELECTRON})', linewidth=2)
    
    ax1.set_xlabel('Mode Number Difference Δn', fontsize=12, fontweight='bold')
    ax1.set_ylabel('Geometric Overlap |<n|n+Δn>|', fontsize=12, fontweight='bold')
    ax1.set_title('Transition Matrix Elements', fontsize=14, fontweight='bold')
    ax1.legend(fontsize=11)
    ax1.grid(True, alpha=0.3)
    ax1.set_yscale('log')
    
    # Plot 2: Lifetime vs initial mode
    ax2 = axes[0, 1]
    modes = np.arange(5, 150)
    lifetimes = []
    
    for n in modes:
        # Calculate mass from mode number
        mass = M_ELECTRON * (n / N_ELECTRON)**2
        tau = model.predict_lifetime(mass, M_ELECTRON, n, N_ELECTRON, 
                                     include_weak=True)
        lifetimes.append(tau)
    
    ax2.plot(modes, lifetimes, 'b-', linewidth=2)
    ax2.scatter([N_MUON], [TAU_MUON], s=200, c='green', edgecolors='black',
               linewidth=2, zorder=5, label='Muon (measured)')
    ax2.scatter([N_TAU], [TAU_TAU], s=200, c='red', edgecolors='black',
               linewidth=2, zorder=5, label='Tau (measured)')
    
    ax2.set_xlabel('Initial Mode Number n', fontsize=12, fontweight='bold')
    ax2.set_ylabel('Lifetime (seconds)', fontsize=12, fontweight='bold')
    ax2.set_title('Predicted Lifetimes for Higher Modes', fontsize=14, fontweight='bold')
    ax2.set_yscale('log')
    ax2.legend(fontsize=11)
    ax2.grid(True, alpha=0.3)
    
    # Plot 3: Energy-lifetime relationship
    ax3 = axes[1, 0]
    masses_ratio = np.logspace(0, 4, 100)  # Relative to electron
    masses = M_ELECTRON * masses_ratio
    modes_from_mass = N_ELECTRON * np.sqrt(masses_ratio)
    
    lifetimes_vs_mass = []
    for m, n in zip(masses, modes_from_mass):
        tau = model.predict_lifetime(m, M_ELECTRON, n, N_ELECTRON,
                                     include_weak=True)
        lifetimes_vs_mass.append(tau)
    
    ax3.plot(masses_ratio, lifetimes_vs_mass, 'b-', linewidth=2)
    ax3.scatter([M_MUON/M_ELECTRON], [TAU_MUON], s=200, c='green',
               edgecolors='black', linewidth=2, zorder=5, label='Muon')
    ax3.scatter([M_TAU/M_ELECTRON], [TAU_TAU], s=200, c='red',
               edgecolors='black', linewidth=2, zorder=5, label='Tau')
    
    ax3.set_xlabel('Mass / Electron Mass', fontsize=12, fontweight='bold')
    ax3.set_ylabel('Lifetime (seconds)', fontsize=12, fontweight='bold')
    ax3.set_title('Lifetime vs Mass Scaling', fontsize=14, fontweight='bold')
    ax3.set_xscale('log')
    ax3.set_yscale('log')
    ax3.legend(fontsize=11)
    ax3.grid(True, alpha=0.3)
    
    # Plot 4: Summary text
    ax4 = axes[1, 1]
    ax4.axis('off')
    
    summary = """
DECAY RATE PREDICTIONS

Key Results:
• Geometric transitions: n₂ → n₁
• Rate ∝ (ΔE)³ × |<n₁|n₂>|²
• Selection rules from overlap

Muon Decay (μ → e):
  Δn = 27 (large jump)
  Predicted: Calculate from geometry
  Measured: 2.197 μs
  
Tau Decay (τ → e/μ):
  Multiple channels
  Faster due to larger mass
  Measured: 290 fs

Next: Refine weak coupling
to match measured lifetimes
    """
    
    ax4.text(0.1, 0.9, summary, transform=ax4.transAxes,
            fontsize=11, verticalalignment='top', family='monospace',
            bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.7))
    
    plt.tight_layout()
    plt.savefig('/mnt/user-data/outputs/decay_rates_analysis.png', dpi=150)
    print("\nDecay rate visualization saved!")


if __name__ == "__main__":
    print("="*70)
    print("GEOMETRIC DECAY RATE PREDICTIONS")
    print("Testing: Can we predict particle lifetimes from geometry?")
    print("="*70)
    
    model = GeometricDecayModel()
    
    # Analyze muon
    tau_muon_pred = model.analyze_muon_decay()
    
    # Analyze tau
    tau_tau_pred = model.analyze_tau_decay()
    
    # Branching ratios
    predictor = BranchingRatioPredictor()
    predictor.tau_branching_ratios()
    
    # Visualize
    print("\n" + "="*70)
    print("CREATING VISUALIZATIONS")
    print("="*70)
    visualize_decay_landscape()
    
    print("\n" + "="*70)
    print("SUMMARY")
    print("="*70)
    print("\nThe geometric model provides a framework for calculating")
    print("decay rates from mode transitions. The actual predictions")
    print("depend on:")
    print("  1. Mode overlap integrals (selection rules)")
    print("  2. Weak force coupling strength")
    print("  3. Phase space factors")
    print("\nFurther refinement needed to match experimental lifetimes,")
    print("but the geometric structure is in place!")
