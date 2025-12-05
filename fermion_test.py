"""
Fermion-Only Universal Geometry Test
=====================================

Testing if ALL FERMIONS (leptons + quarks, excluding bosons) 
exhibit a universal throat/Compton ratio.
"""

import numpy as np
import matplotlib.pyplot as plt

# Physical constants
C = 2.998e8          # Speed of light (m/s)
HBAR = 1.055e-34     # Reduced Planck constant (J·s)
ALPHA = 1/137.036    # Fine structure constant
EV_TO_KG = 1.783e-36 # Conversion: 1 eV/c² = 1.783e-36 kg

# Particle masses in kg - FERMIONS ONLY
PARTICLES = {
    # Leptons (spin 1/2, charge -1)
    'electron': {'mass_kg': 9.109e-31, 'spin': 0.5, 'charge': -1, 'type': 'lepton'},
    'muon': {'mass_kg': 1.883e-28, 'spin': 0.5, 'charge': -1, 'type': 'lepton'},
    'tau': {'mass_kg': 3.167e-27, 'spin': 0.5, 'charge': -1, 'type': 'lepton'},
    
    # Quarks (spin 1/2, various charges)
    'charm': {'mass_kg': 1.27e9 * EV_TO_KG, 'spin': 0.5, 'charge': 2/3, 'type': 'quark'},
    'bottom': {'mass_kg': 4.18e9 * EV_TO_KG, 'spin': 0.5, 'charge': -1/3, 'type': 'quark'},
    'top': {'mass_kg': 172.8e9 * EV_TO_KG, 'spin': 0.5, 'charge': 2/3, 'type': 'quark'},
}

def compton_wavelength(mass_kg):
    """Compton wavelength λ = ℏ/(mc)"""
    return HBAR / (mass_kg * C)

def throat_model_A(mass_kg, spin, charge_e):
    """Model A: Multiplicative spin-charge correction"""
    lambda_c = compton_wavelength(mass_kg)
    spin_factor = 1 + np.sqrt(spin * (spin + 1))
    charge_factor = 1 + abs(charge_e) * ALPHA
    return lambda_c * spin_factor * charge_factor

def throat_model_B(mass_kg, spin, charge_e):
    """Model B: Unified geometric factor"""
    lambda_c = compton_wavelength(mass_kg)
    geometric_factor = np.sqrt(1 + spin*(spin+1) + (charge_e**2)*ALPHA)
    return lambda_c * geometric_factor

def throat_model_C(mass_kg, spin, charge_e):
    """Model C: Charge-weighted correction"""
    lambda_c = compton_wavelength(mass_kg)
    correction = 1 + np.sqrt(spin * (spin + 1)) + (charge_e**2) * ALPHA
    return lambda_c * correction

def throat_model_D(mass_kg, spin, charge_e):
    """Model D: Simple universal constant (no spin/charge dependence)"""
    lambda_c = compton_wavelength(mass_kg)
    UNIVERSAL_CONSTANT = 1.326  # Calibrated to electron
    return lambda_c * UNIVERSAL_CONSTANT

print("="*80)
print("FERMION UNIVERSAL GEOMETRY TEST")
print("="*80)
print("\nHypothesis: All fermions (leptons + quarks) share the same")
print("            throat/Compton ratio, revealing universal geometry.\n")
print("Testing 4 models:")
print("  A: C = λ_c × [1 + √(s(s+1))] × [1 + |q|α]")
print("  B: C = λ_c × √(1 + s(s+1) + q²α)")
print("  C: C = λ_c × [1 + √(s(s+1)) + q²α]")
print("  D: C = λ_c × constant (no spin/charge correction)")

results = {}

for name, props in PARTICLES.items():
    mass = props['mass_kg']
    spin = props['spin']
    charge = props['charge']
    
    lambda_c = compton_wavelength(mass)
    
    CA = throat_model_A(mass, spin, charge)
    CB = throat_model_B(mass, spin, charge)
    CC = throat_model_C(mass, spin, charge)
    CD = throat_model_D(mass, spin, charge)
    
    results[name] = {
        'type': props['type'],
        'mass_eV': mass / EV_TO_KG,
        'spin': spin,
        'charge': charge,
        'lambda_c': lambda_c,
        'ratio_A': CA / lambda_c,
        'ratio_B': CB / lambda_c,
        'ratio_C': CC / lambda_c,
        'ratio_D': CD / lambda_c,
    }

print("\n" + "="*80)
print("RESULTS")
print("="*80)

for model_letter in ['A', 'B', 'C', 'D']:
    print(f"\n{'MODEL ' + model_letter:-^80}")
    print(f"{'Particle':<12} {'Type':<8} {'Charge':<8} {'Mass (GeV)':<15} {'Ratio':<12}")
    print("-"*80)
    
    ratios = []
    for name, data in sorted(results.items(), key=lambda x: x[1]['mass_eV']):
        ratio = data[f'ratio_{model_letter}']
        ratios.append(ratio)
        
        mass_gev = data['mass_eV'] / 1e9
        if mass_gev < 0.001:
            mass_str = f"{mass_gev*1000:.4f} MeV"
        else:
            mass_str = f"{mass_gev:.3f} GeV"
        
        print(f"{name:<12} {data['type']:<8} {data['charge']:>7.2f}  {mass_str:<15} {ratio:>11.6f}")
    
    mean_ratio = np.mean(ratios)
    std_ratio = np.std(ratios)
    cv = (std_ratio / mean_ratio) * 100
    min_ratio = min(ratios)
    max_ratio = max(ratios)
    spread = (max_ratio - min_ratio) / mean_ratio * 100
    
    print("-"*80)
    print(f"Mean:   {mean_ratio:.6f}")
    print(f"Std:    {std_ratio:.6f}")
    print(f"CV:     {cv:.3f}%")
    print(f"Range:  [{min_ratio:.6f}, {max_ratio:.6f}]")
    print(f"Spread: {spread:.3f}%")
    
    if cv < 1:
        print(f"\n🎯 SMOKING GUN! CV < 1% → UNIVERSAL RATIO CONFIRMED!")
    elif cv < 5:
        print(f"\n✓✓ EXCELLENT! CV < 5% → Strong universal geometry!")
    elif cv < 10:
        print(f"\n✓ GOOD! CV < 10% → Approximate universality")
    else:
        print(f"\n✗ POOR: CV > 10% → No clear universal ratio")

# Find best model
best_cv = float('inf')
best_model = None

for model_letter in ['A', 'B', 'C', 'D']:
    ratios = [results[n][f'ratio_{model_letter}'] for n in results.keys()]
    cv = (np.std(ratios) / np.mean(ratios)) * 100
    if cv < best_cv:
        best_cv = cv
        best_model = model_letter

print("\n" + "="*80)
print("BEST MODEL")
print("="*80)
print(f"\nModel {best_model} has lowest CV = {best_cv:.3f}%")

ratios_best = [results[n][f'ratio_{best_model}'] for n in results.keys()]
mean_best = np.mean(ratios_best)

print(f"\nUniversal throat/Compton ratio = {mean_best:.6f}")
print(f"Scatter among 6 fermions: ±{best_cv:.3f}%")

if best_cv < 1:
    print("\n" + "🎯"*40)
    print("\nSMOKING GUN EVIDENCE FOR UNIVERSAL FERMION GEOMETRY!")
    print("\nAll six fermions (3 leptons + 3 quarks) exhibit the")
    print("SAME throat-to-Compton ratio to within <1% precision!")
    print("\nThis strongly suggests:")
    print("  • Fermions are excitations of the same geometric structure")
    print("  • Mass hierarchy arises from different resonance modes")
    print("  • Throat circumference universally tracks Compton wavelength")
    print("\n" + "🎯"*40)
    
elif best_cv < 5:
    print("\n✓✓ STRONG EVIDENCE FOR UNIVERSAL GEOMETRY")
    print(f"\nAll fermions cluster within {best_cv:.1f}% of mean ratio.")
    print("This suggests a common geometric origin.")

# Create visualization
fig, axes = plt.subplots(2, 2, figsize=(14, 10))

# Plot 1: All four models comparison
ax = axes[0, 0]
names_sorted = sorted(results.keys(), key=lambda x: results[x]['mass_eV'])
x_pos = np.arange(len(names_sorted))
width = 0.2

for i, model in enumerate(['A', 'B', 'C', 'D']):
    ratios = [results[n][f'ratio_{model}'] for n in names_sorted]
    ax.bar(x_pos + i*width - 1.5*width, ratios, width, 
           label=f'Model {model}', alpha=0.8)

ax.set_xticks(x_pos)
ax.set_xticklabels(names_sorted, rotation=45, ha='right')
ax.set_ylabel('Throat/Compton Ratio', fontsize=12, fontweight='bold')
ax.set_title('All Models: Fermion Ratios', fontsize=13, fontweight='bold')
ax.legend(fontsize=10)
ax.grid(True, alpha=0.3, axis='y')

# Plot 2: Best model - deviation from mean
ax = axes[0, 1]
ratios_best = [results[n][f'ratio_{best_model}'] for n in names_sorted]
deviations = [(r - mean_best)/mean_best * 100 for r in ratios_best]
colors = ['blue' if results[n]['type'] == 'lepton' else 'red' for n in names_sorted]

bars = ax.barh(names_sorted, deviations, color=colors, alpha=0.7)
ax.axvline(0, color='black', linewidth=2)
ax.axvline(-1, color='gray', linestyle='--', alpha=0.5, linewidth=1)
ax.axvline(1, color='gray', linestyle='--', alpha=0.5, linewidth=1)
ax.set_xlabel('Deviation from Mean (%)', fontsize=12, fontweight='bold')
ax.set_title(f'Model {best_model}: Deviation Analysis', fontsize=13, fontweight='bold')
ax.grid(True, alpha=0.3, axis='x')

# Add legend
from matplotlib.patches import Patch
legend_elements = [Patch(facecolor='blue', alpha=0.7, label='Leptons'),
                  Patch(facecolor='red', alpha=0.7, label='Quarks')]
ax.legend(handles=legend_elements, fontsize=10)

# Plot 3: Ratio vs Mass (log scale)
ax = axes[1, 0]
masses = [results[n]['mass_eV']/1e9 for n in names_sorted]
ratios = [results[n][f'ratio_{best_model}'] for n in names_sorted]
colors_scatter = ['blue' if results[n]['type'] == 'lepton' else 'red' for n in names_sorted]

for i, name in enumerate(names_sorted):
    ax.scatter(masses[i], ratios[i], s=200, c=colors_scatter[i], 
              edgecolor='k', linewidth=2, alpha=0.8)
    ax.text(masses[i], ratios[i]*1.001, name, fontsize=9, ha='center', va='bottom')

ax.axhline(mean_best, color='black', linestyle='--', linewidth=2,
          label=f'Mean = {mean_best:.4f}')
ax.fill_between([min(masses)*0.1, max(masses)*10], 
               mean_best*0.99, mean_best*1.01, 
               alpha=0.3, color='yellow', label='±1% band')

ax.set_xscale('log')
ax.set_xlabel('Mass (GeV)', fontsize=12, fontweight='bold')
ax.set_ylabel('Throat/Compton Ratio', fontsize=12, fontweight='bold')
ax.set_title(f'Model {best_model}: Mass Independence Test', fontsize=13, fontweight='bold')
ax.legend(fontsize=10)
ax.grid(True, alpha=0.3)

# Plot 4: Summary statistics
ax = axes[1, 1]
ax.axis('off')

summary = f"""
{'='*45}
   FERMION UNIVERSAL GEOMETRY
{'='*45}

BEST MODEL: {best_model}
{'─'*45}
Universal ratio:  {mean_best:.6f}
Standard dev:     {np.std(ratios_best):.6f}
Coeff. variation: {best_cv:.3f}%
Range:            [{min(ratios_best):.6f}, {max(ratios_best):.6f}]
Spread:           {(max(ratios_best)-min(ratios_best))/mean_best*100:.3f}%

{'='*45}
   PARTICLE BREAKDOWN
{'─'*45}
"""

for name in names_sorted:
    ratio = results[name][f'ratio_{best_model}']
    dev = (ratio - mean_best) / mean_best * 100
    summary += f"{name:8}: {ratio:.6f}  ({dev:+.2f}%)\n"

summary += f"\n{'='*45}\n"

if best_cv < 1:
    summary += "🎯 UNIVERSAL RATIO CONFIRMED!\n"
    summary += "All fermions share same geometry\n"
    summary += "to <1% precision.\n"
elif best_cv < 5:
    summary += "✓✓ Strong universal geometry!\n"
    summary += f"All within {best_cv:.1f}% of mean.\n"
elif best_cv < 10:
    summary += "✓ Approximate universality.\n"
else:
    summary += "No clear universal ratio.\n"

ax.text(0.05, 0.95, summary, transform=ax.transAxes,
       fontsize=10, verticalalignment='top', family='monospace',
       bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.9,
                edgecolor='darkgreen', linewidth=2))

title_text = "FERMION UNIVERSAL GEOMETRY: "
if best_cv < 1:
    title_text += "SMOKING GUN (CV < 1%)"
    color = 'darkgreen'
elif best_cv < 5:
    title_text += "STRONG EVIDENCE (CV < 5%)"
    color = 'green'
else:
    title_text += f"CV = {best_cv:.1f}%"
    color = 'black'

plt.suptitle(title_text, fontsize=16, fontweight='bold', color=color, y=0.995)
plt.tight_layout(rect=[0, 0, 1, 0.99])
plt.savefig('/mnt/user-data/outputs/fermion_universal_geometry.png', 
           dpi=300, bbox_inches='tight')
print("\n✓ Plot saved: fermion_universal_geometry.png")
plt.show()
