"""
Quark Mass Predictions from Geometric Resonances
=================================================

If leptons are wormhole throats with mode numbers determining mass,
what about QUARKS?

Key question: Are quarks the SAME geometric structure as leptons,
or do they have a different throat topology?

Hypothesis 1: Quarks are similar throats but with:
  - Different charge (fractional: +2/3 or -1/3)
  - Color charge (SU(3) instead of U(1))
  - Confined (can't exist alone)

Hypothesis 2: Quarks have HIGHER mode numbers than leptons
  - Up/Down: low modes (like electron)
  - Strange/Charm: medium modes (like muon)
  - Bottom/Top: high modes (like tau and beyond)

Let's test this!
"""

import numpy as np
import matplotlib.pyplot as plt

# Physical constants
C = 2.998e8
HBAR = 1.055e-34
M_ELECTRON = 9.109e-31

# Quark masses (current masses, not constituent masses)
# These are the "bare" quark masses from QCD
QUARK_MASSES = {
    'up': 2.16e-30,      # ~2.2 MeV/c^2
    'down': 4.67e-30,    # ~4.7 MeV/c^2
    'strange': 9.3e-29,  # ~95 MeV/c^2
    'charm': 1.27e-27,   # ~1.27 GeV/c^2
    'bottom': 4.18e-27,  # ~4.18 GeV/c^2
    'top': 1.73e-25,     # ~173 GeV/c^2
}

# Lepton reference
N_ELECTRON = 2  # Mode number
N_MUON = 29
N_TAU = 118


def compton_wavelength(m_kg):
    return HBAR / (m_kg * C)


class QuarkGeometricModel:
    """
    Test if quarks fit the same geometric resonance pattern as leptons.
    """
    
    def __init__(self, scaling_law='quadratic'):
        """
        scaling_law: 'linear', 'quadratic', or 'geometric_mean'
        """
        self.scaling_law = scaling_law
        self.reference_mass = M_ELECTRON
        self.reference_mode = N_ELECTRON
        
    def mass_from_mode(self, n):
        """
        Calculate mass from mode number using chosen scaling law.
        """
        if self.scaling_law == 'linear':
            return self.reference_mass * (n / self.reference_mode)
        elif self.scaling_law == 'quadratic':
            return self.reference_mass * (n / self.reference_mode)**2
        elif self.scaling_law == 'geometric_mean':
            return self.reference_mass * (n / self.reference_mode)**1.5
        else:
            return self.reference_mass * (n / self.reference_mode)**2
    
    def mode_from_mass(self, mass):
        """
        Infer mode number from mass using chosen scaling law.
        """
        if self.scaling_law == 'linear':
            return self.reference_mode * (mass / self.reference_mass)
        elif self.scaling_law == 'quadratic':
            return self.reference_mode * np.sqrt(mass / self.reference_mass)
        elif self.scaling_law == 'geometric_mean':
            return self.reference_mode * (mass / self.reference_mass)**(2/3)
        else:
            return self.reference_mode * np.sqrt(mass / self.reference_mass)
    
    def analyze_quark_spectrum(self):
        """
        Analyze all quarks and infer their mode numbers.
        """
        print("\n" + "="*80)
        print("QUARK SPECTRUM ANALYSIS")
        print("="*80)
        print(f"\nUsing scaling law: {self.scaling_law}")
        print(f"Reference: electron at n={self.reference_mode}, m={self.reference_mass:.3e} kg")
        
        print("\n" + "-"*80)
        print(f"{'Quark':<10} {'Mass (kg)':<15} {'Mass (MeV)':<12} {'Mode n':<10} {'m/m_e':<12}")
        print("-"*80)
        
        quark_modes = {}
        
        for name, mass in sorted(QUARK_MASSES.items(), key=lambda x: x[1]):
            n = self.mode_from_mass(mass)
            mass_mev = mass * C**2 / 1.602e-13  # Convert to MeV
            ratio_to_electron = mass / M_ELECTRON
            
            quark_modes[name] = n
            
            print(f"{name:<10} {mass:<15.3e} {mass_mev:<12.1f} {n:<10.1f} {ratio_to_electron:<12.1f}")
        
        return quark_modes
    
    def compare_generations(self, quark_modes):
        """
        Compare quark generations to lepton generations.
        """
        print("\n" + "="*80)
        print("GENERATION STRUCTURE COMPARISON")
        print("="*80)
        
        print("\nLEPTONS:")
        print(f"  1st gen: electron  (n={N_ELECTRON})")
        print(f"  2nd gen: muon      (n={N_MUON})")
        print(f"  3rd gen: tau       (n={N_TAU})")
        
        print("\nQUARKS:")
        print(f"  1st gen: up        (n={quark_modes['up']:.1f})")
        print(f"          down      (n={quark_modes['down']:.1f})")
        print(f"  2nd gen: charm     (n={quark_modes['charm']:.1f})")
        print(f"          strange   (n={quark_modes['strange']:.1f})")
        print(f"  3rd gen: top       (n={quark_modes['top']:.1f})")
        print(f"          bottom    (n={quark_modes['bottom']:.1f})")
        
        # Look for patterns
        print("\n" + "-"*80)
        print("PATTERN ANALYSIS")
        print("-"*80)
        
        # Check if mode numbers cluster by generation
        gen1_quarks = [quark_modes['up'], quark_modes['down']]
        gen2_quarks = [quark_modes['charm'], quark_modes['strange']]
        gen3_quarks = [quark_modes['top'], quark_modes['bottom']]
        
        print(f"\nGeneration 1 modes: {gen1_quarks[0]:.1f}, {gen1_quarks[1]:.1f}")
        print(f"Generation 2 modes: {gen2_quarks[0]:.1f}, {gen2_quarks[1]:.1f}")
        print(f"Generation 3 modes: {gen3_quarks[0]:.1f}, {gen3_quarks[1]:.1f}")
        
        # Compare to lepton modes
        print(f"\nLepton-Quark correspondence:")
        print(f"  Electron (n={N_ELECTRON}) ← → Up/Down (n~{np.mean(gen1_quarks):.1f})")
        print(f"  Muon (n={N_MUON}) ← → Charm/Strange (n~{np.mean(gen2_quarks):.1f})")
        print(f"  Tau (n={N_TAU}) ← → Top/Bottom (n~{np.mean(gen3_quarks):.1f})")
        
        # Check ratios
        print(f"\nMode number ratios:")
        ratio_12 = np.mean(gen2_quarks) / np.mean(gen1_quarks)
        ratio_23 = np.mean(gen3_quarks) / np.mean(gen2_quarks)
        ratio_13 = np.mean(gen3_quarks) / np.mean(gen1_quarks)
        
        print(f"  Gen2/Gen1: {ratio_12:.2f}")
        print(f"  Gen3/Gen2: {ratio_23:.2f}")
        print(f"  Gen3/Gen1: {ratio_13:.2f}")
        
        # Compare to lepton ratios
        lepton_ratio_12 = N_MUON / N_ELECTRON
        lepton_ratio_23 = N_TAU / N_MUON
        
        print(f"\nLepton ratios for comparison:")
        print(f"  μ/e: {lepton_ratio_12:.2f}")
        print(f"  τ/μ: {lepton_ratio_23:.2f}")
    
    def test_mass_ratios(self, quark_modes):
        """
        Test if quark mass ratios follow geometric patterns.
        """
        print("\n" + "="*80)
        print("QUARK MASS RATIO TESTS")
        print("="*80)
        
        # Test some key ratios
        ratios = {
            'charm/up': (QUARK_MASSES['charm'], QUARK_MASSES['up']),
            'bottom/strange': (QUARK_MASSES['bottom'], QUARK_MASSES['strange']),
            'top/charm': (QUARK_MASSES['top'], QUARK_MASSES['charm']),
            'strange/down': (QUARK_MASSES['strange'], QUARK_MASSES['down']),
        }
        
        print("\n" + "-"*80)
        print(f"{'Ratio':<20} {'Measured':<12} {'From Modes':<15} {'Error %':<10}")
        print("-"*80)
        
        for name, (m1, m2) in ratios.items():
            measured_ratio = m1 / m2
            
            q1_name, q2_name = name.split('/')
            n1 = quark_modes[q1_name]
            n2 = quark_modes[q2_name]
            
            # Predicted ratio from mode numbers
            if self.scaling_law == 'quadratic':
                predicted_ratio = (n1 / n2)**2
            elif self.scaling_law == 'linear':
                predicted_ratio = n1 / n2
            else:
                predicted_ratio = (n1 / n2)**1.5
            
            error = abs(predicted_ratio - measured_ratio) / measured_ratio * 100
            
            print(f"{name:<20} {measured_ratio:<12.1f} {predicted_ratio:<15.1f} {error:<10.1f}")


def visualize_quark_spectrum():
    """
    Create comprehensive visualization of quark spectrum.
    """
    fig, axes = plt.subplots(2, 2, figsize=(16, 12))
    
    # Test all three scaling laws
    models = {
        'linear': QuarkGeometricModel('linear'),
        'quadratic': QuarkGeometricModel('quadratic'),
        'geometric': QuarkGeometricModel('geometric_mean'),
    }
    
    # Plot 1: Masses vs Mode Numbers (all scaling laws)
    ax1 = axes[0, 0]
    
    for scaling, model in models.items():
        quark_modes = {}
        masses = []
        modes = []
        
        for name, mass in QUARK_MASSES.items():
            n = model.mode_from_mass(mass)
            quark_modes[name] = n
            masses.append(mass)
            modes.append(n)
        
        ax1.scatter(modes, masses, s=150, alpha=0.7, label=scaling)
    
    # Add leptons for reference
    ax1.scatter([N_ELECTRON, N_MUON, N_TAU], 
               [M_ELECTRON, 1.883e-28, 3.167e-27],
               s=200, marker='s', c='black', edgecolors='red', linewidth=2,
               label='leptons', zorder=5)
    
    ax1.set_xlabel('Mode Number n', fontsize=13, fontweight='bold')
    ax1.set_ylabel('Mass (kg)', fontsize=13, fontweight='bold')
    ax1.set_title('Quark Masses vs Mode Numbers', fontsize=15, fontweight='bold')
    ax1.set_yscale('log')
    ax1.legend(fontsize=11)
    ax1.grid(True, alpha=0.3)
    
    # Plot 2: Generation structure
    ax2 = axes[0, 1]
    
    model_quad = models['quadratic']
    quark_modes = {name: model_quad.mode_from_mass(mass) 
                   for name, mass in QUARK_MASSES.items()}
    
    generations = {
        'Gen 1': ['up', 'down'],
        'Gen 2': ['charm', 'strange'],
        'Gen 3': ['top', 'bottom']
    }
    
    colors = {'Gen 1': 'blue', 'Gen 2': 'green', 'Gen 3': 'red'}
    
    x_pos = 0
    for gen, quarks in generations.items():
        for quark in quarks:
            mass = QUARK_MASSES[quark]
            ax2.bar(x_pos, mass, color=colors[gen], alpha=0.7, 
                   edgecolor='black', linewidth=2)
            ax2.text(x_pos, mass*1.5, quark, ha='center', fontsize=10,
                    fontweight='bold')
            ax2.text(x_pos, mass*0.3, f'n={quark_modes[quark]:.0f}',
                    ha='center', fontsize=9, style='italic')
            x_pos += 1
        x_pos += 0.5  # Gap between generations
    
    ax2.set_yscale('log')
    ax2.set_ylabel('Mass (kg)', fontsize=13, fontweight='bold')
    ax2.set_title('Quark Generations', fontsize=15, fontweight='bold')
    ax2.set_xticks([])
    ax2.grid(True, alpha=0.3, axis='y')
    
    # Plot 3: Mass ratios comparison
    ax3 = axes[1, 0]
    
    # Key mass ratios
    ratio_names = ['top/bottom', 'charm/strange', 'strange/down']
    measured = [
        QUARK_MASSES['top'] / QUARK_MASSES['bottom'],
        QUARK_MASSES['charm'] / QUARK_MASSES['strange'],
        QUARK_MASSES['strange'] / QUARK_MASSES['down'],
    ]
    
    predicted = []
    for ratio_name in ratio_names:
        q1, q2 = ratio_name.split('/')
        n1 = quark_modes[q1]
        n2 = quark_modes[q2]
        predicted.append((n1/n2)**2)
    
    x = np.arange(len(ratio_names))
    width = 0.35
    
    ax3.bar(x - width/2, measured, width, label='Measured', color='steelblue',
           edgecolor='black', linewidth=2)
    ax3.bar(x + width/2, predicted, width, label='Geometric', color='coral',
           edgecolor='black', linewidth=2)
    
    ax3.set_ylabel('Mass Ratio', fontsize=13, fontweight='bold')
    ax3.set_title('Quark Mass Ratio Predictions', fontsize=15, fontweight='bold')
    ax3.set_xticks(x)
    ax3.set_xticklabels(ratio_names)
    ax3.legend(fontsize=11)
    ax3.grid(True, alpha=0.3, axis='y')
    
    # Plot 4: Unified spectrum
    ax4 = axes[1, 1]
    
    # All particles together
    all_particles = {
        'electron': (N_ELECTRON, M_ELECTRON, 'blue', 'lepton'),
        'muon': (N_MUON, 1.883e-28, 'blue', 'lepton'),
        'tau': (N_TAU, 3.167e-27, 'blue', 'lepton'),
    }
    
    for name, mass in QUARK_MASSES.items():
        all_particles[name] = (quark_modes[name], mass, 'red', 'quark')
    
    for name, (n, m, color, ptype) in all_particles.items():
        marker = 's' if ptype == 'lepton' else 'o'
        ax4.scatter(n, m, s=150, c=color, marker=marker, alpha=0.7,
                   edgecolors='black', linewidth=1.5)
        if name in ['electron', 'top', 'tau']:
            ax4.text(n*1.1, m*1.5, name, fontsize=9)
    
    # Fit line
    modes_all = [data[0] for data in all_particles.values()]
    masses_all = [data[1] for data in all_particles.values()]
    mode_range = np.logspace(np.log10(min(modes_all)), np.log10(max(modes_all)), 100)
    mass_fit = M_ELECTRON * (mode_range / N_ELECTRON)**2
    
    ax4.plot(mode_range, mass_fit, 'k--', linewidth=2, alpha=0.5, 
            label='m ∝ n² (quadratic)')
    
    ax4.set_xlabel('Mode Number n', fontsize=13, fontweight='bold')
    ax4.set_ylabel('Mass (kg)', fontsize=13, fontweight='bold')
    ax4.set_title('Unified Lepton-Quark Spectrum', fontsize=15, fontweight='bold')
    ax4.set_xscale('log')
    ax4.set_yscale('log')
    ax4.legend(fontsize=11)
    ax4.grid(True, alpha=0.3)
    
    # Add legend for particle types
    from matplotlib.patches import Patch
    legend_elements = [
        Patch(facecolor='blue', label='Leptons'),
        Patch(facecolor='red', label='Quarks')
    ]
    ax4.legend(handles=legend_elements, loc='upper left', fontsize=11)
    
    plt.tight_layout()
    plt.savefig('/mnt/user-data/outputs/quark_spectrum_analysis.png', dpi=150)
    print("\nQuark spectrum visualization saved!")


if __name__ == "__main__":
    print("="*80)
    print("QUARK GEOMETRIC RESONANCE ANALYSIS")
    print("Testing: Do quarks follow the same geometric pattern as leptons?")
    print("="*80)
    
    # Test with quadratic scaling (best for leptons)
    model = QuarkGeometricModel('quadratic')
    quark_modes = model.analyze_quark_spectrum()
    model.compare_generations(quark_modes)
    model.test_mass_ratios(quark_modes)
    
    # Visualize
    print("\n" + "="*80)
    print("CREATING VISUALIZATIONS")
    print("="*80)
    visualize_quark_spectrum()
    
    print("\n" + "="*80)
    print("CONCLUSIONS")
    print("="*80)
    print("\nIf quarks follow the same geometric pattern:")
    print("  • They would be wormhole throats like leptons")
    print("  • Color charge = different throat topology")
    print("  • Generations align approximately")
    print("  • But masses span a MUCH wider range")
    print("\nThe top quark (173 GeV) requires mode n~800!")
    print("This suggests either:")
    print("  1. Quarks use a different scaling law, or")
    print("  2. QCD effects modify the bare geometric masses")
