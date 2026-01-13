import numpy as np
import matplotlib.pyplot as plt

# --- PHYSICS ENGINE ---
def run_simulation(v0, angle_deg, m, Cd, A, rho=1.225, g=9.81, dt=0.005):
    angle_rad = np.radians(angle_deg)
    vx = v0 * np.cos(angle_rad)
    vy = v0 * np.sin(angle_rad)
    
    curr_x, curr_y = 0.0, 0.0
    x_pts, y_pts = [0.0], [0.0]
    
    while curr_y >= 0:
        v = np.sqrt(vx**2 + vy**2)
        if v > 1e-6:
            Fd = 0.5 * rho * v**2 * Cd * A
            ax = -(Fd * (vx / v)) / m
            ay = -g - (Fd * (vy / v)) / m
        else:
            ax, ay = 0, -g
        
        vx += ax * dt
        vy += ay * dt
        curr_x += vx * dt
        curr_y += vy * dt
        
        if curr_y >= 0:
            x_pts.append(curr_x)
            y_pts.append(curr_y)
            
    return x_pts, y_pts

def find_optimal_angle(v0, m, Cd, A):
    best_angle = 0
    max_range = 0
    for angle in np.arange(1, 90, 0.5):
        x, _ = run_simulation(v0, angle, m, Cd, A)
        if x[-1] > max_range:
            max_range = x[-1]
            best_angle = angle
    return best_angle, max_range

# --- MAIN INTERFACE ---
def main():
    print("=== PROJECTILE MOTION OPTIMIZER ===")
    print("Choose an object preset:")
    print("1. Cricket Ball (Leather)")
    print("2. Golf Ball (Dimpled)")
    print("3. Football (Soccer Ball)")
    print("4. Manual Input (Custom)")
    
    choice = input("\nSelect (1-4): ")

    # Preset Data
    if choice == '1':
        name, m, Cd, A = "Cricket Ball", 0.160, 0.42, 0.00396
    elif choice == '2':
        name, m, Cd, A = "Golf Ball", 0.0459, 0.24, 0.00143
    elif choice == '3':
        name, m, Cd, A = "Football", 0.430, 0.25, 0.038
    else:
        name = "Custom Object"
        m = float(input("Enter Mass (kg): "))
        Cd = float(input("Enter Drag Coefficient (Cd): "))
        A = float(input("Enter Cross-sectional Area (m^2): "))

    v0 = float(input("\nEnter Initial Velocity (m/s): "))
    user_angle = float(input("Enter your Test Angle (degrees): "))

    print(f"\nSimulating {name}...")

    # Calculations
    opt_angle, _ = find_optimal_angle(v0, m, Cd, A)
    
    x_user, y_user = run_simulation(v0, user_angle, m, Cd, A)
    x_45, y_45 = run_simulation(v0, 45, m, Cd, A)
    x_opt, y_opt = run_simulation(v0, opt_angle, m, Cd, A)

    # Output Data
    print("-" * 30)
    print(f"{'Scenario':<20}  | {'Range (m)':<10}")
    print("-" * 30)
    print(f"{'User Angle ('+str(user_angle)+'°)':<20}  | {x_user[-1]:.2f}")
    print(f"{'Standard 45°':<20}  | {x_45[-1]:.2f}")
    print(f"{'Optimal Angle ('+str(opt_angle)+'°)':<20} | {x_opt[-1]:.2f}")
    print("-" * 30)

    # Visualization
    plt.figure(figsize=(12, 6))
    plt.plot(x_user, y_user, label=f"User Angle: {user_angle}°", linestyle='--', color='gray')
    plt.plot(x_45, y_45, label="Standard 45°", color='blue', alpha=0.5)
    plt.plot(x_opt, y_opt, label=f"Optimal Angle: {opt_angle}°", color='red', linewidth=2)
    
    plt.title(f"Trajectory Comparison: {name} at {v0} m/s")
    plt.xlabel("Distance (meters)")
    plt.ylabel("Height (meters)")
    plt.axhline(0, color='black', lw=1)
    plt.legend()
    plt.grid(True, linestyle=':', alpha=0.6)
    plt.show()

if __name__ == "__main__":
    main()