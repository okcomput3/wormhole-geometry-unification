"""
Kerr-Newman Black Hole Geometry and Wormhole Throat Stability
===============================================================

This module implements the mathematics of rotating, charged micro-black-holes
(Kerr-Newman geometry) to test the hypothesis that particle masses correspond
to geometric stability resonances in wormhole throat configurations.

Physical Constants (SI units)
"""

import numpy as np
from scipy.optimize import fsolve, minimize
from scipy.integrate import odeint
import matplotlib.pyplot as plt

# Physical constants
C = 2.998e8          # Speed of light (m/s)
G = 6.674e-11        # Gravitational constant (m^3 kg^-1 s^-2)
HBAR = 1.055e-34     # Reduced Planck constant (J·s)
K_E = 8.988e9        # Coulomb constant (N·m^2·C^-2)
ALPHA = 1/137.036    # Fine structure constant
M_PLANCK = 2.176e-8  # Planck mass (kg)
L_PLANCK = 1.616e-35 # Planck length (m)
E_PLANCK = 1.956e9   # Planck energy (J)

# Known particle masses (kg)
M_ELECTRON = 9.109e-31
M_MUON = 1.883e-28
M_TAU = 3.167e-27
M_PROTON = 1.673e-27

# Derived units for micro-black-holes
def geometric_mass(m_kg):
    """Convert mass in kg to geometric units (length)"""
    return G * m_kg / C**2

def compton_wavelength(m_kg):
    """Compton wavelength of a particle"""
    return HBAR / (m_kg * C)

def schwarzschild_radius(m_kg):
    """Schwarzschild radius for given mass"""
    return 2 * G * m_kg / C**2


class KerrNewmanBlackHole:
    """
    Kerr-Newman black hole with mass M, angular momentum J, and charge Q.
    
    The Kerr-Newman metric describes a rotating, charged black hole.
    For micro-black-holes, we hypothesize these parameters correspond to
    particle properties: mass, spin, and charge.
    """
    
    def __init__(self, mass_kg, spin=0.5, charge_e=1.0, quantum_corrected=True):
        """
        Initialize Kerr-Newman black hole
        
        Parameters:
        -----------
        mass_kg : float
            Mass in kilograms
        spin : float
            Spin quantum number (0.5 for fermions, 1 for bosons, etc.)
        charge_e : float
            Charge in units of elementary charge
        quantum_corrected : bool
            If True, use Compton wavelength as effective size (for quantum particles)
        """
        self.m_kg = mass_kg
        self.spin = spin
        self.charge_e = charge_e
        self.quantum_corrected = quantum_corrected
        
        # For quantum particles, use Compton wavelength as effective "size"
        # This represents quantum smearing of the would-be singularity
        if quantum_corrected:
            lambda_c = compton_wavelength(mass_kg)
            # Effective geometric mass scaled by quantum effects
            self.M = lambda_c / (2 * np.pi)  # Use Compton as fundamental scale
            self.a = spin * HBAR / (mass_kg * C)  # Angular momentum
            # Scale charge to match quantum regime
            self.Q = charge_e * HBAR / (mass_kg * C) * np.sqrt(ALPHA)
        else:
            # Classical Kerr-Newman
            self.M = geometric_mass(mass_kg)
            self.a = spin * HBAR / (mass_kg * C)
            self.Q = charge_e * np.sqrt(K_E * G) / C**2
        
        # Key radii
        self.r_plus = self.outer_horizon()
        self.r_minus = self.inner_horizon()
        self.r_ergosphere = self.ergosphere_radius()
        
    def outer_horizon(self):
        """Outer event horizon radius"""
        return self.M + np.sqrt(self.M**2 - self.a**2 - self.Q**2)
    
    def inner_horizon(self):
        """Inner (Cauchy) horizon radius"""
        return self.M - np.sqrt(self.M**2 - self.a**2 - self.Q**2)
    
    def ergosphere_radius(self, theta=np.pi/2):
        """Ergosphere radius at angle theta"""
        return self.M + np.sqrt(self.M**2 - self.a**2 * np.cos(theta)**2 - self.Q**2)
    
    def is_physical(self):
        """Check if black hole parameters are physical (not naked singularity)"""
        return self.M**2 >= self.a**2 + self.Q**2
    
    def throat_geometry(self, r):
        """
        Wormhole throat geometry metric component.
        Returns the 'radius' of a circular cross-section at coordinate r.
        """
        if r < self.r_minus:
            return np.nan
        
        delta = r**2 - 2*self.M*r + self.a**2 + self.Q**2
        rho2 = r**2 + self.a**2 * np.cos(np.pi/2)**2  # At equator
        
        # Throat circumference / 2π
        return np.sqrt(rho2)
    
    def effective_potential(self, r, l=0):
        """
        Effective potential for wormhole throat oscillations.
        
        Parameters:
        -----------
        r : float
            Radial coordinate
        l : int
            Angular momentum quantum number
        """
        if r <= self.r_plus:
            return np.inf
        
        # Simplified effective potential for radial perturbations
        delta = r**2 - 2*self.M*r + self.a**2 + self.Q**2
        
        # Centrifugal barrier + geometry
        V_eff = (l * (l + 1) / r**2 + 
                 (2*self.M - r) / r**3 + 
                 self.Q**2 / r**4)
        
        return V_eff


class WormholeThroatResonance:
    """
    Models wormhole throat stability and resonance conditions.
    
    The hypothesis: stable throat configurations correspond to allowed
    particle masses. The throat must form standing waves, similar to
    atomic orbitals but in the geometry itself.
    """
    
    def __init__(self, black_hole):
        self.bh = black_hole
        
    def throat_oscillation_frequency(self, n=1):
        """
        Calculate characteristic oscillation frequency for throat mode n.
        
        This is analogous to atomic energy levels, but for geometric modes.
        """
        # Characteristic frequency from black hole parameters
        omega_0 = C**3 / (G * self.bh.m_kg)
        
        # Mode-dependent frequency (quantum numbers)
        # This is where the geometry determines allowed energies
        omega_n = omega_0 * np.sqrt(n * (n + 1)) / (2 * np.pi)
        
        return omega_n
    
    def stability_condition(self, mass_kg, n=1, l=0):
        """
        Check if a given mass produces a stable throat configuration.
        
        Stability requires:
        1. Black hole must be physical (no naked singularity)
        2. Throat must support standing wave modes
        3. Energy must match throat oscillation quantum
        """
        bh = KerrNewmanBlackHole(mass_kg, spin=self.bh.spin, charge_e=self.bh.charge_e)
        
        if not bh.is_physical():
            return False, np.inf
        
        # Calculate throat resonance energy
        omega = self.throat_oscillation_frequency(n)
        E_resonance = HBAR * omega
        
        # Compare to particle rest mass energy
        E_particle = mass_kg * C**2
        
        # Stability metric: how well does resonance match mass?
        delta_E = abs(E_resonance - E_particle) / E_particle
        
        return delta_E < 0.1, delta_E  # 10% tolerance for now
    
    def find_resonant_masses(self, mass_range=(1e-33, 1e-25), n_modes=5):
        """
        Search for masses that produce stable throat resonances.
        
        Returns:
        --------
        resonant_masses : list
            Masses (in kg) that satisfy stability conditions
        """
        masses = np.logspace(np.log10(mass_range[0]), 
                           np.log10(mass_range[1]), 
                           1000)
        
        resonant_masses = []
        
        for n in range(1, n_modes + 1):
            for mass in masses:
                stable, delta = self.stability_condition(mass, n=n)
                if stable:
                    resonant_masses.append((mass, n, delta))
        
        return resonant_masses


def calculate_mass_ratios(masses):
    """Calculate ratios between consecutive masses"""
    ratios = []
    for i in range(len(masses) - 1):
        ratio = masses[i+1] / masses[i]
        ratios.append(ratio)
    return ratios


def compare_to_known_particles(predicted_masses):
    """
    Compare predicted masses to known particles.
    
    Known ratios:
    - muon/electron ≈ 206.77
    - tau/muon ≈ 16.82
    - tau/electron ≈ 3477
    """
    known_particles = {
        'electron': M_ELECTRON,
        'muon': M_MUON,
        'tau': M_TAU
    }
    
    print("\n" + "="*60)
    print("COMPARISON TO KNOWN PARTICLES")
    print("="*60)
    
    print(f"\nKnown mass ratios:")
    print(f"  muon/electron = {M_MUON/M_ELECTRON:.2f}")
    print(f"  tau/muon = {M_TAU/M_MUON:.2f}")
    print(f"  tau/electron = {M_TAU/M_ELECTRON:.2f}")
    
    if len(predicted_masses) >= 2:
        pred_ratios = calculate_mass_ratios(predicted_masses)
        print(f"\nPredicted mass ratios:")
        for i, ratio in enumerate(pred_ratios):
            print(f"  m_{i+2}/m_{i+1} = {ratio:.2f}")
    
    print("\nClosest matches:")
    for name, known_mass in known_particles.items():
        closest = min(predicted_masses, key=lambda x: abs(x - known_mass))
        error = abs(closest - known_mass) / known_mass * 100
        print(f"  {name}: predicted {closest:.3e} kg vs actual {known_mass:.3e} kg ({error:.1f}% error)")


if __name__ == "__main__":
    print("Kerr-Newman Micro-Black-Hole Resonance Model")
    print("=" * 60)
    print("\nTesting hypothesis: Particle masses correspond to geometric")
    print("resonances in wormhole throat configurations.")
    print()
    
    # Test with electron-like parameters
    print("Creating electron-like micro-black-hole...")
    electron_bh = KerrNewmanBlackHole(M_ELECTRON, spin=0.5, charge_e=-1)
    
    print(f"  Mass: {electron_bh.m_kg:.3e} kg")
    print(f"  Geometric mass M: {electron_bh.M:.3e} m")
    print(f"  Angular parameter a: {electron_bh.a:.3e} m")
    print(f"  Outer horizon r+: {electron_bh.r_plus:.3e} m")
    print(f"  Compton wavelength: {compton_wavelength(M_ELECTRON):.3e} m")
    print(f"  Physical? {electron_bh.is_physical()}")
    
    # Search for resonances
    print("\nSearching for resonant throat configurations...")
    resonance = WormholeThroatResonance(electron_bh)
    resonant_masses = resonance.find_resonant_masses(
        mass_range=(M_ELECTRON/10, M_TAU*10),
        n_modes=3
    )
    
    if resonant_masses:
        print(f"\nFound {len(resonant_masses)} resonant configurations:")
        unique_masses = sorted(list(set([m for m, n, d in resonant_masses])))
        
        for i, mass in enumerate(unique_masses[:10]):  # Show first 10
            print(f"  Mode {i+1}: {mass:.3e} kg ({mass/M_ELECTRON:.1f} × electron mass)")
        
        # Compare to known particles
        compare_to_known_particles(unique_masses[:5])
    else:
        print("\nNo resonances found in search range.")
        print("Model parameters may need refinement.")
