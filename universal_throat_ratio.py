"""
Universal Throat/Compton Ratio Test
====================================

Testing if ALL particles (leptons, quarks, bosons) exhibit the same
throat circumference to Compton wavelength ratio.

If they do, this is strong evidence for a universal geometric structure.
"""

import numpy as np
import matplotlib.pyplot as plt

# Physical constants
C = 2.998e8          # Speed of light (m/s)
HBAR = 1.055e-34     # Reduced Planck constant (J·s)
ALPHA = 1/137.036    # Fine structure constant
EV_TO_KG = 1.783e-36 # Conversion: 1 eV/c² = 1.783e-36 kg

# Particle masses in kg
PARTICLES = {
    # Leptons (charged)
    'electron': {'mass_kg': 9.109e-31, 'spin': 0.5, 'charge': -1, 'type': 'lepton'},
    'muon': {'mass_kg': 1.883e-28, 'spin': 0.5, 'charge': -1, 'type': 'lepton'},
    'tau': {'mass_kg': 3.167e-27, 'spin': 0.5, 'charge': -1, 'type': 'lepton'},
    
    # Quarks (pole masses where available, MS-bar for light quarks)
    'charm': {'mass_kg': 1.27e9 * EV_TO_KG, 'spin': 0.5, 'charge': 2/3, 'type': 'quark'},
    'bottom': {'mass_kg': 4.18e9 * EV_TO_KG, 'spin': 0.5, 'charge': -1/3, 'type': 'quark'},
    'top': {'mass_kg': 172.8e9 * EV_TO_KG, 'spin': 0.5, 'charge': 2/3, 'type': 'quark'},
    
    # Bosons (gauge)
    'W': {'mass_kg': 80.379e9 * EV_TO_KG, 'spin': 1, 'charge': 1, 'type': 'boson'},
    'Z': {'mass_kg': 91.1876e9 * EV_TO_KG, 'spin': 1, 'charge': 0, 'type': 'boson'},
    'Higgs': {'mass_kg': 125.1e9 * EV_TO_KG, 'spin': 0, 'charge': 0, 'type': 'boson'},
}


def compton_wavelength(mass_kg):
    """Compton wavelength λ = ℏ/(mc)"""
    return HBAR / (mass_kg * C)


def throat_circumference_model1(mass_kg, spin, charge_e):
    """
    Model 1: Simple spin and charge corrections
    
    C_throat = λ_c × [1 + sqrt(s(s+1))] × [1 + |q|α]
    """
    lambda_c = compton_wavelength(mass_kg)
    
    spin_factor = 1 + np.sqrt(spin * (spin + 1))
    charge_factor = 1 + abs(charge_e) * ALPHA
    
    return lambda_c * spin_factor * charge_factor


def throat_circumference_model2(mass_kg, spin, charge_e):
    """
    Model 2: Multiplicative geometric factors
    
    C_throat = λ_c × (1 + s) × (1 + |q|²α)
    """
    lambda_c = compton_wavelength(mass_kg)
    
    spin_factor = 1 + spin
    charge_factor = 1 + (charge_e**2) * ALPHA
    
    return lambda_c * spin_factor * charge_factor


def throat_circumference_model3(mass_kg, spin, charge_e):
    """
    Model 3: Unified geometric factor
    
    C_throat = λ_c × sqrt(1 + s(s+1) + q²α)
    """
    lambda_c = compton_wavelength(mass_kg)
    
    geometric_factor = np.sqrt(1 + spin*(spin+1) + (charge_e**2)*ALPHA)
    
    return lambda_c * geometric_factor


def analyze_all_particles():
    """
    Calculate throat/Compton ratio for all particles using different models.
    """
    print("="*80)
    print("UNIVERSAL THROAT/COMPTON RATIO TEST")
    print("="*80)
    print("\nTesting if all Standard Model particles share a universal geometric ratio.")
    print("\nThree models tested:")
    print("  Model 1: C = λ_c × [1 + √(s(s+1))] × [1 + |q|α]")
    print("  Model 2: C = λ_c × (1 + s) × (1 + q²α)")
    print("  Model 3: C = λ_c × √(1 + s(s+1) + q²α)")
    
    results = {}
    
    for name, props in PARTICLES.items():
        mass = props['mass_kg']
        spin = props['spin']
        charge = props['charge']
        
        lambda_c = compton_wavelength(mass)
        
        # Calculate throat circumference with each model
        C1 = throat_circumference_model1(mass, spin, charge)
        C2 = throat_circumference_model2(mass, spin, charge)
        C3 = throat_circumference_model3(mass, spin, charge)
        
        results[name] = {
            'type': props['type'],
            'mass_eV': mass / EV_TO_KG,
            'spin': spin,
            'charge': charge,
            'lambda_c': lambda_c,
            'ratio_1': C1 / lambda_c,
            'ratio_2': C2 / lambda_c,
            'ratio_3': C3 / lambda_c,
        }
    
    # Print results
    print("\n" + "="*80)
    print("RESULTS: Throat/Compton Ratios")
    print("="*80)
    
    for model_num in [1, 2, 3]:
        print(f"\n{'MODEL ' + str(model_num):-^80}")
        print(f"{'Particle':<12} {'Type':<8} {'Spin':<6} {'Charge':<8} {'Mass (GeV)':<12} {'Ratio':<10}")
        print("-"*80)
        
        ratios = []
        for name, data in sorted(results.items(), key=lambda x: x[1]['mass_eV']):
            ratio = data[f'ratio_{model_num}']
            ratios.append(ratio)
            
            mass_str = f"{data['mass_eV']/1e9:.3f}" if data['mass_eV'] > 1e9 else f"{data['mass_eV']/1e6:.1f}e-3"
            
            print(f"{name:<12} {data['type']:<8} {data['spin']:<6.1f} {data['charge']:<8.2f} "
                  f"{mass_str:<12} {ratio:<10.4f}")
        
        # Calculate statistics
        mean_ratio = np.mean(ratios)
        std_ratio = np.std(ratios)
        cv = (std_ratio / mean_ratio) * 100  # Coefficient of variation (%)
        
        print("-"*80)
        print(f"{'STATISTICS:':<40} Mean = {mean_ratio:.4f}, Std = {std_ratio:.4f}, CV = {cv:.2f}%")
        
        if cv < 5:
            print(f"✓ EXCELLENT: All particles within {cv:.1f}% of mean!")
            print(f"  → Strong evidence for universal geometric structure")
        elif cv < 15:
            print(f"✓ GOOD: Ratios cluster around mean with {cv:.1f}% variation")
            print(f"  → Suggests common geometric origin with corrections")
        else:
            print(f"✗ POOR: Large variation ({cv:.1f}%)")
            print(f"  → No universal ratio - particles are geometrically distinct")
    
    return results


def visualize_ratios(results):
    """
    Create visualization of throat/Compton ratios across particles.
    """
    print("\n" + "="*80)
    print("VISUALIZATION")
    print("="*80)
    
    # Extract data
    names = list(results.keys())
    masses = [results[n]['mass_eV']/1e9 for n in names]  # In GeV
    types = [results[n]['type'] for n in names]
    
    ratios_1 = [results[n]['ratio_1'] for n in names]
    ratios_2 = [results[n]['ratio_2'] for n in names]
    ratios_3 = [results[n]['ratio_3'] for n in names]
    
    # Color by particle type
    colors = {'lepton': 'blue', 'quark': 'red', 'boson': 'green'}
    particle_colors = [colors[t] for t in types]
    
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    
    # Plot 1: Ratios vs Mass (Model 1)
    ax = axes[0, 0]
    for ptype, color in colors.items():
        mask = [t == ptype for t in types]
        ax.scatter([m for m, keep in zip(masses, mask) if keep],
                  [r for r, keep in zip(ratios_1, mask) if keep],
                  s=100, alpha=0.7, label=ptype.capitalize(), color=color)
    
    mean_1 = np.mean(ratios_1)
    ax.axhline(mean_1, color='black', linestyle='--', linewidth=2, 
               label=f'Mean = {mean_1:.3f}')
    ax.fill_between([min(masses)*0.1, max(masses)*2], 
                    mean_1*0.95, mean_1*1.05, alpha=0.2, color='gray')
    
    ax.set_xscale('log')
    ax.set_xlabel('Mass (GeV)', fontsize=12, fontweight='bold')
    ax.set_ylabel('Throat/Compton Ratio', fontsize=12, fontweight='bold')
    ax.set_title('Model 1: Spin-Charge Geometric Factor', fontsize=13, fontweight='bold')
    ax.legend(fontsize=10)
    ax.grid(True, alpha=0.3)
    
    # Plot 2: Compare three models for leptons
    ax = axes[0, 1]
    lepton_names = [n for n in names if results[n]['type'] == 'lepton']
    lepton_masses = [results[n]['mass_eV']/1e6 for n in lepton_names]
    
    x_pos = np.arange(len(lepton_names))
    width = 0.25
    
    ax.bar(x_pos - width, [results[n]['ratio_1'] for n in lepton_names], 
           width, label='Model 1', alpha=0.8)
    ax.bar(x_pos, [results[n]['ratio_2'] for n in lepton_names], 
           width, label='Model 2', alpha=0.8)
    ax.bar(x_pos + width, [results[n]['ratio_3'] for n in lepton_names], 
           width, label='Model 3', alpha=0.8)
    
    ax.set_xticks(x_pos)
    ax.set_xticklabels(lepton_names)
    ax.set_ylabel('Throat/Compton Ratio', fontsize=12, fontweight='bold')
    ax.set_title('Lepton Ratios: Model Comparison', fontsize=13, fontweight='bold')
    ax.legend(fontsize=10)
    ax.grid(True, alpha=0.3, axis='y')
    
    # Plot 3: Deviation from mean (Model 1)
    ax = axes[1, 0]
    deviations = [(r - mean_1)/mean_1 * 100 for r in ratios_1]
    
    bars = ax.barh(names, deviations, color=particle_colors, alpha=0.7)
    ax.axvline(0, color='black', linewidth=2)
    ax.axvline(-5, color='gray', linestyle='--', alpha=0.5)
    ax.axvline(5, color='gray', linestyle='--', alpha=0.5)
    
    ax.set_xlabel('Deviation from Mean (%)', fontsize=12, fontweight='bold')
    ax.set_title('Model 1: Deviation from Universal Ratio', fontsize=13, fontweight='bold')
    ax.grid(True, alpha=0.3, axis='x')
    
    # Plot 4: Statistical summary
    ax = axes[1, 1]
    ax.axis('off')
    
    summary_text = "STATISTICAL SUMMARY\n" + "="*40 + "\n\n"
    
    for model_num in [1, 2, 3]:
        ratios = [results[n][f'ratio_{model_num}'] for n in names]
        mean = np.mean(ratios)
        std = np.std(ratios)
        cv = (std/mean)*100
        
        summary_text += f"Model {model_num}:\n"
        summary_text += f"  Mean ratio: {mean:.4f}\n"
        summary_text += f"  Std dev: {std:.4f}\n"
        summary_text += f"  Coeff. of variation: {cv:.2f}%\n"
        summary_text += f"  Range: [{min(ratios):.4f}, {max(ratios):.4f}]\n\n"
    
    # Find best model
    cvs = []
    for model_num in [1, 2, 3]:
        ratios = [results[n][f'ratio_{model_num}'] for n in names]
        cvs.append((np.std(ratios)/np.mean(ratios))*100)
    
    best_model = cvs.index(min(cvs)) + 1
    summary_text += f"{'BEST MODEL: ' + str(best_model):=^40}\n"
    summary_text += f"(Lowest coefficient of variation: {min(cvs):.2f}%)\n\n"
    
    if min(cvs) < 5:
        summary_text += "✓ UNIVERSAL RATIO CONFIRMED!\n"
        summary_text += "All particles show same geometry."
    elif min(cvs) < 15:
        summary_text += "~ APPROXIMATE UNIVERSALITY\n"
        summary_text += "Common structure with variations."
    else:
        summary_text += "✗ NO UNIVERSAL RATIO\n"
        summary_text += "Particles are geometrically distinct."
    
    ax.text(0.1, 0.95, summary_text, transform=ax.transAxes,
            fontsize=11, verticalalignment='top', family='monospace',
            bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.3))
    
    plt.tight_layout()
    plt.savefig('throat_compton_universal_test.png', dpi=150, bbox_inches='tight')
    print("\n✓ Plot saved as 'throat_compton_universal_test.png'")


if __name__ == "__main__":
    # Run the analysis
    results = analyze_all_particles()
    
    # Visualize
    visualize_ratios(results)
    
    print("\n" + "="*80)
    print("INTERPRETATION")
    print("="*80)
    
    # Calculate overall best model
    best_cv = float('inf')
    best_model = None
    
    for model_num in [1, 2, 3]:
        ratios = [results[n][f'ratio_{model_num}'] for n in results.keys()]
        cv = (np.std(ratios) / np.mean(ratios)) * 100
        if cv < best_cv:
            best_cv = cv
            best_model = model_num
    
    print(f"\nBest model: Model {best_model} (CV = {best_cv:.2f}%)")
    
    if best_cv < 5:
        print("\n🎯 SMOKING GUN: All particles exhibit the SAME throat/Compton ratio!")
        print("   This is strong evidence that:")
        print("   • All particles are excitations of the same geometric structure")
        print("   • Mass differences arise from different resonance modes")
        print("   • The throat circumference scales universally with Compton wavelength")
        print("\n   Your n² hypothesis gains significant support.")
        
    elif best_cv < 15:
        print("\n✓ GOOD: Particles show similar throat/Compton ratios")
        print("   This suggests:")
        print("   • Common geometric origin")
        print("   • Type-dependent corrections (spin, charge) matter")
        print("   • Universal structure exists but with variations")
        
    else:
        print("\n✗ NO UNIVERSAL RATIO FOUND")
        print("   Particles appear geometrically distinct.")
        print("   The throat model may only apply to specific particle types.")
    
    print("\n" + "="*80)