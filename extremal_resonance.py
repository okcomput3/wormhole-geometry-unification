"""
Extremal Geometric Resonance Model
===================================

Key insight: Elementary particles exist in the EXTREMAL regime where
angular momentum and charge are comparable to or exceed the mass parameter.

In this regime, classical black hole horizons disappear, but the geometry
creates stable wormhole-like throat structures. These are NOT classical
black holes - they're quantum geometric objects.

The stability conditions for these throats determine allowed masses.
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import minimize, fsolve

# Physical constants
C = 2.998e8
HBAR = 1.055e-34
ALPHA = 1/137.036
M_ELECTRON = 9.109e-31
M_MUON = 1.883e-28
M_TAU = 3.167e-27


def compton_wavelength(m_kg):
    """Compton wavelength - the fundamental quantum scale for a particle"""
    return HBAR / (m_kg * C)


class ExtremalGeometricResonance:
    """
    Model for particles as extremal geometric structures.
    
    In the extremal limit (a ~ M, Q ~ M), the would-be black hole
    becomes a naked singularity in classical GR. BUT in quantum geometry,
    this creates a stable wormhole throat structure.
    
    The key: Treat the Compton wavelength as the fundamental geometric
    scale, and derive stability conditions from throat oscillation modes.
    """
    
    def __init__(self, spin=0.5, charge_e=1):
        """
        Initialize for a given spin and charge.
        
        Parameters:
        -----------
        spin : float
            Spin quantum number (0.5, 1, 1.5, etc.)
        charge_e : float
            Charge in units of elementary charge
        """
        self.spin = spin
        self.charge_e = charge_e
        
    def throat_circumference(self, mass_kg):
        """
        Effective throat circumference at the Compton scale.
        
        For extremal geometry, the throat size is set by quantum mechanics,
        not classical gravity.
        """
        lambda_c = compton_wavelength(mass_kg)
        
        # The throat circumference includes contributions from:
        # 1. Compton wavelength (quantum scale)
        # 2. Spin-induced stretching
        # 3. Charge-induced expansion
        
        # Spin stretching factor
        spin_factor = 1 + (self.spin * (self.spin + 1))**0.5
        
        # Charge expansion (from electromagnetic stress-energy)
        charge_factor = 1 + abs(self.charge_e) * ALPHA
        
        return lambda_c * spin_factor * charge_factor
    
    def throat_energy_density(self, mass_kg):
        """
        Energy density in the wormhole throat.
        
        This represents the geometric stress-energy that holds the throat open.
        """
        circumference = self.throat_circumference(mass_kg)
        
        # Energy is distributed around the throat
        # Use electromagnetic and rotational contributions
        E_em = (self.charge_e * ALPHA * HBAR * C) / circumference
        E_rot = (self.spin * HBAR**2) / (mass_kg * circumference**2)
        
        return (E_em + E_rot) / circumference
    
    def stability_parameter(self, mass_kg, mode_n=1):
        """
        Calculate stability parameter for throat oscillation mode n.
        
        Stable throats have integer or half-integer mode numbers.
        The throat must support standing wave patterns.
        
        Returns:
        --------
        S : float
            Stability parameter. S ≈ 0 indicates a resonance.
        """
        circumference = self.throat_circumference(mass_kg)
        
        # Wavelength of mode n
        lambda_mode = circumference / mode_n
        
        # Corresponding energy quantum
        E_mode = HBAR * C / lambda_mode
        
        # Rest energy of particle
        E_rest = mass_kg * C**2
        
        # Stability: how well does geometric resonance match particle energy?
        # The throat is stable when its oscillation modes match the rest energy
        S = abs(E_mode - E_rest) / E_rest
        
        return S
    
    def find_resonant_mass(self, mode_n=1, initial_guess=M_ELECTRON):
        """
        Find the mass that creates a stable throat resonance for mode n.
        
        This solves: E_mode(m) = m*c^2
        
        Returns:
        --------
        mass_kg : float
            Resonant mass, or None if no solution found
        """
        def residual(log_mass):
            mass = 10**log_mass
            return self.stability_parameter(mass, mode_n)
        
        try:
            result = minimize(residual, np.log10(initial_guess), method='Nelder-Mead')
            if result.fun < 0.01:  # 1% tolerance
                return 10**result.x[0]
            else:
                return None
        except:
            return None
    
    def scan_mass_spectrum(self, n_modes=10, mass_range=(1e-32, 1e-25)):
        """
        Scan through mode numbers to find all stable throat configurations.
        
        Returns:
        --------
        spectrum : list of (mass_kg, mode_n, stability)
        """
        spectrum = []
        
        masses = np.logspace(np.log10(mass_range[0]), 
                           np.log10(mass_range[1]), 
                           500)
        
        for n in range(1, n_modes + 1):
            # For each mode, find where stability is best
            stabilities = [self.stability_parameter(m, n) for m in masses]
            
            # Find local minima (resonances)
            for i in range(1, len(stabilities) - 1):
                if stabilities[i] < stabilities[i-1] and stabilities[i] < stabilities[i+1]:
                    if stabilities[i] < 0.05:  # 5% tolerance
                        spectrum.append((masses[i], n, stabilities[i]))
        
        return sorted(spectrum, key=lambda x: x[0])


class MassRatioPredictor:
    """
    Predicts mass ratios from geometric resonance theory.
    
    Key hypothesis: The ratio between particle masses should follow
    from the ratio of throat resonance modes.
    """
    
    def __init__(self):
        pass
    
    def geometric_ratio(self, n1, n2, spin=0.5):
        """
        Predict mass ratio for mode n2 relative to mode n1.
        
        For simple circular throat resonances:
        m2/m1 ≈ (n2/n1)^α where α depends on geometry
        
        The exponent α encodes how energy scales with mode number.
        """
        # Different scaling possibilities:
        # α = 1: linear (simple standing wave)
        # α = 2: quadratic (like atomic orbitals)
        # α = 3/2: intermediate (could arise from 3D geometry)
        
        # Test multiple scenarios
        ratios = {
            'linear': n2 / n1,
            'quadratic': (n2 / n1)**2,
            'geometric_mean': (n2 / n1)**1.5,
            'spin_modified': (n2 / n1)**(1 + spin),
        }
        
        return ratios
    
    def compare_to_leptons(self):
        """
        Compare geometric predictions to known lepton masses.
        """
        print("\n" + "="*70)
        print("GEOMETRIC MASS RATIO PREDICTIONS vs KNOWN LEPTONS")
        print("="*70)
        
        # Known ratios
        r_mu_e = M_MUON / M_ELECTRON  # ≈ 206.77
        r_tau_mu = M_TAU / M_MUON      # ≈ 16.82
        r_tau_e = M_TAU / M_ELECTRON   # ≈ 3477
        
        print(f"\nKnown mass ratios:")
        print(f"  μ/e  = {r_mu_e:.2f}")
        print(f"  τ/μ  = {r_tau_mu:.2f}")
        print(f"  τ/e  = {r_tau_e:.2f}")
        
        # Test if any mode combinations match
        print(f"\nSearching for mode combinations that match...")
        
        best_matches = []
        
        for n1 in range(1, 20):
            for n2 in range(n1+1, 30):
                ratios = self.geometric_ratio(n1, n2)
                
                for name, ratio in ratios.items():
                    # Check muon/electron
                    error_mu = abs(ratio - r_mu_e) / r_mu_e
                    if error_mu < 0.1:  # Within 10%
                        best_matches.append(('μ/e', n1, n2, name, ratio, error_mu))
                    
                    # Check tau/muon
                    error_tau_mu = abs(ratio - r_tau_mu) / r_tau_mu
                    if error_tau_mu < 0.1:
                        best_matches.append(('τ/μ', n1, n2, name, ratio, error_tau_mu))
        
        if best_matches:
            print(f"\nFound {len(best_matches)} potential matches:")
            for pair, n1, n2, scaling, ratio, error in sorted(best_matches, key=lambda x: x[5])[:10]:
                print(f"  {pair}: n={n1}→{n2}, {scaling:15s}, ratio={ratio:6.1f}, error={error*100:.1f}%")
        else:
            print("\nNo close matches found with simple mode ratios.")
            print("More complex geometric factors may be needed.")


def visualize_stability_landscape():
    """Create visualization of where stable resonances occur"""
    print("\n" + "="*70)
    print("STABILITY LANDSCAPE ANALYSIS")
    print("="*70)
    
    model = ExtremalGeometricResonance(spin=0.5, charge_e=-1)
    
    # Create mass range around electron-muon-tau
    masses = np.logspace(np.log10(M_ELECTRON/2), np.log10(M_TAU*2), 300)
    
    plt.figure(figsize=(12, 8))
    
    # Plot stability parameter for different modes
    for n in [1, 2, 3, 5, 8]:
        stabilities = [model.stability_parameter(m, n) for m in masses]
        plt.plot(masses, stabilities, label=f'mode n={n}', linewidth=2)
    
    # Mark known particle masses
    plt.axvline(M_ELECTRON, color='blue', linestyle='--', alpha=0.5, label='electron')
    plt.axvline(M_MUON, color='green', linestyle='--', alpha=0.5, label='muon')
    plt.axvline(M_TAU, color='red', linestyle='--', alpha=0.5, label='tau')
    
    plt.xscale('log')
    plt.yscale('log')
    plt.xlabel('Mass (kg)', fontsize=12)
    plt.ylabel('Stability Parameter S (lower = more stable)', fontsize=12)
    plt.title('Wormhole Throat Stability vs Mass', fontsize=14, fontweight='bold')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    
    plt.savefig('/mnt/user-data/outputs/stability_landscape.png', dpi=150)
    print("\nStability landscape plot saved to outputs/")
    
    return masses, model


if __name__ == "__main__":
    print("="*70)
    print("EXTREMAL GEOMETRIC RESONANCE MODEL")
    print("Testing: Particle masses from wormhole throat stability")
    print("="*70)
    
    # Test the model
    model = ExtremalGeometricResonance(spin=0.5, charge_e=-1)
    
    print("\n1. THROAT GEOMETRY FOR KNOWN PARTICLES")
    print("-" * 70)
    for name, mass in [('electron', M_ELECTRON), ('muon', M_MUON), ('tau', M_TAU)]:
        circ = model.throat_circumference(mass)
        lambda_c = compton_wavelength(mass)
        print(f"\n{name.capitalize()}:")
        print(f"  Mass: {mass:.3e} kg")
        print(f"  Compton wavelength: {lambda_c:.3e} m")
        print(f"  Throat circumference: {circ:.3e} m")
        print(f"  Ratio (throat/Compton): {circ/lambda_c:.2f}")
    
    # Scan for resonances
    print("\n\n2. SCANNING FOR STABLE THROAT RESONANCES")
    print("-" * 70)
    spectrum = model.scan_mass_spectrum(n_modes=15)
    
    if spectrum:
        print(f"\nFound {len(spectrum)} stable configurations:")
        for i, (mass, n, stability) in enumerate(spectrum[:20]):
            ratio_to_electron = mass / M_ELECTRON
            print(f"  #{i+1}: m = {mass:.3e} kg, mode n={n:2d}, "
                  f"S={stability:.4f}, ({ratio_to_electron:6.1f} × m_e)")
    else:
        print("\nNo resonances found. Model needs refinement.")
    
    # Test mass ratio predictions
    print("\n\n3. MASS RATIO PREDICTIONS")
    print("-" * 70)
    predictor = MassRatioPredictor()
    predictor.compare_to_leptons()
    
    # Visualize
    print("\n\n4. VISUALIZATION")
    print("-" * 70)
    visualize_stability_landscape()
    
    print("\n" + "="*70)
    print("Analysis complete!")
    print("="*70)
