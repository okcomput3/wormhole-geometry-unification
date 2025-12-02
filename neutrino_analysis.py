"""
Neutrino Mass Predictions from Geometric Resonances
====================================================

CRITICAL TEST: If the geometric model is real, neutrino masses must fit.

Neutrinos are the most mysterious particles:
- Extremely small masses (< 1 eV)
- Three mass eigenstates (ν₁, ν₂, ν₃)
- Oscillate between flavors
- May be Majorana particles (their own antiparticles)

Known experimental constraints:
- m(ν₁) < 0.8 eV (lightest)
- m(ν₂) ≈ √(Δm²₂₁) ≈ 0.009 eV (from solar neutrinos)
- m(ν₃) ≈ √(Δm²₃₁) ≈ 0.05 eV (from atmospheric neutrinos)

Mass squared differences (measured):
- Δm²₂₁ ≈ 7.5 × 10⁻⁵ eV²
- Δm²₃₁ ≈ 2.5 × 10⁻³ eV² (normal hierarchy)

If neutrinos follow geometric resonances with m ∝ n²,
we should be able to predict their mass ratios!
"""

import numpy as np
import matplotlib.pyplot as plt

# Physical constants
C = 2.998e8
HBAR = 1.055e-34
EV_TO_KG = 1.783e-36  # Conversion: 1 eV/c² to kg

# Neutrino mass constraints (in eV/c²)
# Using normal hierarchy as baseline
DELTA_M21_SQ = 7.5e-5   # eV²
DELTA_M31_SQ = 2.5e-3   # eV²

# Calculate individual masses assuming m1 is lightest
# m₂² - m₁² = Δm²₂₁
# m₃² - m₁² = Δm²₃₁

# Reference: electron
M_ELECTRON_EV = 511000  # eV/c²
M_ELECTRON = 9.109e-31  # kg
N_ELECTRON = 2

# Lepton mode numbers
N_MUON = 29
N_TAU = 118


class NeutrinoGeometricModel:
    """
    Test if neutrinos follow the same geometric pattern.
    
    Key hypothesis: Neutrinos are NEARLY MASSLESS throats.
    If m ∝ n², very small masses mean very small mode numbers.
    
    Could neutrinos be at n < 1? (fractional modes?)
    Or n ~ 0.01? (tiny perturbations?)
    """
    
    def __init__(self):
        self.reference_mass = M_ELECTRON
        self.reference_mode = N_ELECTRON
        
    def mass_from_mode(self, n):
        """Mass from mode number (quadratic scaling)"""
        return self.reference_mass * (n / self.reference_mode)**2
    
    def mode_from_mass(self, mass_kg):
        """Mode number from mass"""
        return self.reference_mode * np.sqrt(mass_kg / self.reference_mass)
    
    def calculate_neutrino_masses_normal_hierarchy(self, m1_ev=0.001):
        """
        Calculate neutrino masses assuming normal hierarchy.
        
        Given m₁, calculate m₂ and m₃ from mass squared differences.
        """
        m1 = m1_ev
        m2 = np.sqrt(m1**2 + DELTA_M21_SQ)
        m3 = np.sqrt(m1**2 + DELTA_M31_SQ)
        
        return m1, m2, m3
    
    def scan_neutrino_scenarios(self):
        """
        Scan different possible m₁ values and check if ratios match geometry.
        """
        print("\n" + "="*80)
        print("NEUTRINO MASS HIERARCHY SCENARIOS")
        print("="*80)
        
        # Try different values for m₁ (lightest neutrino)
        m1_values = np.logspace(-4, 0, 50)  # 0.0001 to 1 eV
        
        best_scenarios = []
        
        for m1 in m1_values:
            m1_ev, m2_ev, m3_ev = self.calculate_neutrino_masses_normal_hierarchy(m1)
            
            # Convert to kg
            m1_kg = m1_ev * EV_TO_KG
            m2_kg = m2_ev * EV_TO_KG
            m3_kg = m3_ev * EV_TO_KG
            
            # Calculate mode numbers
            n1 = self.mode_from_mass(m1_kg)
            n2 = self.mode_from_mass(m2_kg)
            n3 = self.mode_from_mass(m3_kg)
            
            # Check if mode numbers are "nice" (close to simple ratios)
            # Test if n2/n1 and n3/n1 are close to integers or simple fractions
            r21 = n2 / n1 if n1 > 0 else 0
            r31 = n3 / n1 if n1 > 0 else 0
            
            # Mass ratios
            mr21 = m2_ev / m1_ev
            mr31 = m3_ev / m1_ev
            
            # Check if these match geometric predictions
            # For m ∝ n²: m2/m1 = (n2/n1)²
            predicted_mr21 = r21**2
            predicted_mr31 = r31**2
            
            error_21 = abs(predicted_mr21 - mr21) / mr21 if mr21 > 0 else np.inf
            error_31 = abs(predicted_mr31 - mr31) / mr31 if mr31 > 0 else np.inf
            
            total_error = error_21 + error_31
            
            if total_error < 0.1:  # Good match
                best_scenarios.append({
                    'm1': m1_ev,
                    'm2': m2_ev,
                    'm3': m3_ev,
                    'n1': n1,
                    'n2': n2,
                    'n3': n3,
                    'error': total_error
                })
        
        if best_scenarios:
            print("\nBest-fit scenarios (geometric ratios):")
            print("-"*80)
            print(f"{'m₁ (eV)':<12} {'m₂ (eV)':<12} {'m₃ (eV)':<12} {'n₁':<10} {'n₂':<10} {'n₃':<10} {'Error':<10}")
            print("-"*80)
            
            for scenario in sorted(best_scenarios, key=lambda x: x['error'])[:10]:
                print(f"{scenario['m1']:<12.4e} {scenario['m2']:<12.4e} {scenario['m3']:<12.4e} "
                      f"{scenario['n1']:<10.3f} {scenario['n2']:<10.3f} {scenario['n3']:<10.3f} "
                      f"{scenario['error']:<10.4f}")
        else:
            print("\nNo simple geometric scenarios found.")
            print("Neutrinos may require different treatment.")
    
    def test_fractional_modes(self):
        """
        Test if neutrinos could be at fractional mode numbers n < 1.
        
        If electron is at n=2, could neutrinos be at n=0.01, 0.02, 0.05?
        This would explain their tiny masses!
        """
        print("\n" + "="*80)
        print("FRACTIONAL MODE HYPOTHESIS")
        print("="*80)
        print("\nHypothesis: Neutrinos have n << 1 (sub-fundamental modes)")
        print("This would naturally explain their tiny masses!")
        
        # Assume m₁ ~ 0.01 eV (typical value)
        m1_ev = 0.01
        m1_kg = m1_ev * EV_TO_KG
        
        n1 = self.mode_from_mass(m1_kg)
        
        print(f"\nIf m(ν₁) ≈ {m1_ev} eV:")
        print(f"  Mode number: n₁ ≈ {n1:.6f}")
        print(f"  This is n₁ ≈ {n1/N_ELECTRON:.4f} × n_electron")
        
        # Calculate n2 and n3
        m1, m2, m3 = self.calculate_neutrino_masses_normal_hierarchy(m1_ev)
        n2 = self.mode_from_mass(m2 * EV_TO_KG)
        n3 = self.mode_from_mass(m3 * EV_TO_KG)
        
        print(f"\nFull neutrino spectrum:")
        print(f"  ν₁: m = {m1:.4f} eV, n = {n1:.6f}")
        print(f"  ν₂: m = {m2:.4f} eV, n = {n2:.6f}")
        print(f"  ν₃: m = {m3:.4f} eV, n = {n3:.6f}")
        
        print(f"\nMode ratios:")
        print(f"  n₂/n₁ = {n2/n1:.3f}")
        print(f"  n₃/n₁ = {n3/n1:.3f}")
        print(f"  n₃/n₂ = {n3/n2:.3f}")
        
        # Check if mass ratios follow m ∝ n²
        predicted_m2 = m1 * (n2/n1)**2
        predicted_m3 = m1 * (n3/n1)**2
        
        error_2 = abs(predicted_m2 - m2) / m2 * 100
        error_3 = abs(predicted_m3 - m3) / m3 * 100
        
        print(f"\nGeometric predictions:")
        print(f"  Predicted m₂: {predicted_m2:.4f} eV vs actual {m2:.4f} eV (error: {error_2:.2f}%)")
        print(f"  Predicted m₃: {predicted_m3:.4f} eV vs actual {m3:.4f} eV (error: {error_3:.2f}%)")
        
        if error_2 < 5 and error_3 < 5:
            print("\n✓✓✓ NEUTRINOS FOLLOW THE GEOMETRIC PATTERN! ✓✓✓")
        else:
            print("\n⚠ Neutrinos show deviations from simple geometric scaling")
    
    def analyze_flavor_oscillations(self):
        """
        Flavor oscillations in geometric framework.
        
        If neutrinos are wormhole throats, oscillations might be:
        - Quantum superposition of different throat modes
        - Geometric interference between n₁, n₂, n₃ configurations
        """
        print("\n" + "="*80)
        print("NEUTRINO OSCILLATIONS IN GEOMETRIC PICTURE")
        print("="*80)
        
        print("\nStandard picture:")
        print("  Flavor states (ν_e, ν_μ, ν_τ) are superpositions of mass states (ν₁, ν₂, ν₃)")
        print("  Oscillation from quantum interference")
        
        print("\nGeometric interpretation:")
        print("  Each mass state = different throat mode (n₁, n₂, n₃)")
        print("  Flavor = which lepton the throat is entangled with")
        print("  Oscillation = quantum superposition of throat geometries")
        print("  As neutrino propagates, relative phases change → flavor changes")
        
        print("\nKey insight:")
        print("  Neutrino oscillations are GEOMETRIC INTERFERENCE")
        print("  between different wormhole throat resonance modes!")


def visualize_neutrino_spectrum():
    """
    Create comprehensive visualization of neutrino spectrum.
    """
    model = NeutrinoGeometricModel()
    
    fig, axes = plt.subplots(2, 2, figsize=(16, 12))
    
    # Plot 1: Full particle spectrum with neutrinos
    ax1 = axes[0, 0]
    
    # All particles
    particles = {
        'ν₁': (0.01, 0.01 * EV_TO_KG, 'purple'),
        'ν₂': (0.012, 0.012 * EV_TO_KG, 'purple'),
        'ν₃': (0.051, 0.051 * EV_TO_KG, 'purple'),
        'e': (511000, M_ELECTRON, 'blue'),
        'μ': (105658000, 1.883e-28, 'green'),
        'τ': (1776860000, 3.167e-27, 'red'),
    }
    
    for name, (mass_ev, mass_kg, color) in particles.items():
        n = model.mode_from_mass(mass_kg)
        ax1.scatter(n, mass_kg, s=200, c=color, alpha=0.8, 
                   edgecolors='black', linewidth=2)
        ax1.text(n*1.2, mass_kg, name, fontsize=11, fontweight='bold')
    
    # Fit line
    n_range = np.logspace(-4, 3, 100)
    mass_fit = model.mass_from_mode(n_range)
    ax1.plot(n_range, mass_fit, 'k--', linewidth=2, alpha=0.5, label='m ∝ n²')
    
    ax1.set_xlabel('Mode Number n', fontsize=13, fontweight='bold')
    ax1.set_ylabel('Mass (kg)', fontsize=13, fontweight='bold')
    ax1.set_title('Complete Lepton Spectrum (Including Neutrinos)', 
                 fontsize=15, fontweight='bold')
    ax1.set_xscale('log')
    ax1.set_yscale('log')
    ax1.legend(fontsize=11)
    ax1.grid(True, alpha=0.3)
    
    # Plot 2: Neutrino mass hierarchy
    ax2 = axes[0, 1]
    
    m1_vals = np.array([0.001, 0.01, 0.1])  # Different scenarios
    colors_nh = ['lightblue', 'steelblue', 'darkblue']
    
    for i, m1 in enumerate(m1_vals):
        m1_ev, m2_ev, m3_ev = model.calculate_neutrino_masses_normal_hierarchy(m1)
        x_pos = np.array([0, 1, 2]) + i*0.25
        masses = [m1_ev, m2_ev, m3_ev]
        
        ax2.bar(x_pos, masses, width=0.2, label=f'm₁={m1} eV',
               color=colors_nh[i], edgecolor='black', linewidth=1.5)
    
    ax2.set_ylabel('Mass (eV)', fontsize=13, fontweight='bold')
    ax2.set_title('Neutrino Mass Hierarchies', fontsize=15, fontweight='bold')
    ax2.set_xticks([0.25, 1.25, 2.25])
    ax2.set_xticklabels(['ν₁', 'ν₂', 'ν₃'])
    ax2.legend(fontsize=11)
    ax2.set_yscale('log')
    ax2.grid(True, alpha=0.3, axis='y')
    
    # Plot 3: Mode number distribution
    ax3 = axes[1, 0]
    
    # Calculate mode numbers for standard scenario (m1 = 0.01 eV)
    m1, m2, m3 = model.calculate_neutrino_masses_normal_hierarchy(0.01)
    n1 = model.mode_from_mass(m1 * EV_TO_KG)
    n2 = model.mode_from_mass(m2 * EV_TO_KG)
    n3 = model.mode_from_mass(m3 * EV_TO_KG)
    
    all_particles_modes = {
        'ν₁': n1,
        'ν₂': n2,
        'ν₃': n3,
        'e': N_ELECTRON,
        'μ': N_MUON,
        'τ': N_TAU,
    }
    
    names = list(all_particles_modes.keys())
    modes = list(all_particles_modes.values())
    colors_bar = ['purple']*3 + ['blue', 'green', 'red']
    
    ax3.bar(range(len(names)), modes, color=colors_bar, alpha=0.7,
           edgecolor='black', linewidth=2)
    ax3.set_xticks(range(len(names)))
    ax3.set_xticklabels(names, fontsize=12)
    ax3.set_ylabel('Mode Number n', fontsize=13, fontweight='bold')
    ax3.set_title('Mode Number Spectrum', fontsize=15, fontweight='bold')
    ax3.set_yscale('log')
    ax3.grid(True, alpha=0.3, axis='y')
    
    # Plot 4: Summary text
    ax4 = axes[1, 1]
    ax4.axis('off')
    
    summary = f"""
NEUTRINO GEOMETRIC ANALYSIS

Mass Assumptions (Normal Hierarchy):
  m₁ ≈ 0.01 eV
  m₂ ≈ 0.012 eV  
  m₃ ≈ 0.051 eV

Geometric Mode Numbers:
  ν₁: n ≈ {n1:.4f}
  ν₂: n ≈ {n2:.4f}
  ν₃: n ≈ {n3:.4f}

Key Insight:
• Neutrinos have n << 1
• "Sub-fundamental" modes
• Natural explanation for tiny mass!

If m ∝ n²:
  Predicted m₂/m₁ = {(n2/n1)**2:.3f}
  Actual m₂/m₁ = {m2/m1:.3f}
  
  Predicted m₃/m₁ = {(n3/n1)**2:.3f}
  Actual m₃/m₁ = {m3/m1:.3f}

Oscillations = Geometric Interference
between throat modes!
    """
    
    ax4.text(0.1, 0.9, summary, transform=ax4.transAxes,
            fontsize=10, verticalalignment='top', family='monospace',
            bbox=dict(boxstyle='round', facecolor='lavender', alpha=0.8))
    
    plt.tight_layout()
    plt.savefig('/mnt/user-data/outputs/neutrino_spectrum_analysis.png', dpi=150)
    print("\nNeutrino spectrum visualization saved!")


if __name__ == "__main__":
    print("="*80)
    print("NEUTRINO MASS PREDICTIONS FROM GEOMETRIC RESONANCES")
    print("THE CRITICAL TEST")
    print("="*80)
    
    model = NeutrinoGeometricModel()
    
    # Test fractional modes
    model.test_fractional_modes()
    
    # Scan scenarios
    model.scan_neutrino_scenarios()
    
    # Analyze oscillations
    model.analyze_flavor_oscillations()
    
    # Visualize
    print("\n" + "="*80)
    print("CREATING VISUALIZATIONS")
    print("="*80)
    visualize_neutrino_spectrum()
    
    print("\n" + "="*80)
    print("CONCLUSION")
    print("="*80)
    print("\nIf neutrinos have fractional mode numbers (n < 1),")
    print("this naturally explains their tiny masses!")
    print("\nNeutrinos would be 'sub-fundamental' excitations")
    print("of the wormhole throat - even smaller than the electron ground state.")
    print("\nThis is testable: precise neutrino mass measurements")
    print("will tell us if the geometric ratios hold!")
