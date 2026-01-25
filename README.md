# **AeroLaunch - Projectile Motion Optimizer: Beyond the Ideal Vacuum**

## **1. Project Goal**

This goal of this program is to calculate the trajectory of an object
while accounting for the friction and environmental factors it
encounters in the atmosphere. By calculating how air density and wind
speed impact a projectile, we can determine the specific angle required
to achieve the greatest possible distance.

---

## **2. How the Math Works**

In a standard physics classroom, often ignore air resistance (and wind).
However, in this optimizer, we account for two main forces that dictate
where the projectile will land.

### **2.1 Gravity (The Downward Pull)**

Gravity acts constantly on the verical component of the projectile\'s
motion. In this simulation, we use the standard acceleration due to
gravity:

-   $g = 9.81 \ \text{m/s}^2$ : This force pulls the object toward the
    ground, creating the \"arc\" of the flight.

### **2.2 Air Resistance (The Backward Push)**

Air resistance, or drag, pushes against the projectile in the opposite
direction of its motion. Unlike gravity, drag changes based on how fast
the object is moving. It is calculated using:

-   **$\rho$ (Rho) :** The density of the air ($1.225 \, \text{kg/m}^3$
    at sea level).
-   **$v_{rel}$ :** The instantaneous velocity of the projectile
    relative to the wind.
-   **$C_d$ :** The drag coefficient, representing how aerodynamic the
    shape is ($0.47$ for a sphere).
-   **$A$ :** The cross-sectional area of the projectile.

The formula used for the Drag Factor ($F_d$) (later divided by $m$ and
multiplied with components of relative velocity to get $a_x$ and $a_y$)
is:  
$$F_d = \frac{1}{2}\rho v_{rel} C_d A$$

The formula for components of acceleration are:  
$$a_x = -\left(\frac{\rho \, v_{rel} \, C_d A}{2}\right)\cdot \frac{v_{rel\,x}}{m}$$
  
$$a_y = -g - \left(\frac{\rho \, v_{rel} \, C_d A}{2}\right) \cdot \frac{v_{rel\,y}}{m}$$

### **2.3 Calculating Motion Step-by-Step**

Because the drag force depends on the velocity ($v^2$), the math changes
at every instant. We cannot use a single simple formula to find the
landing spot and range. Instead, the program uses the **Euler Method**.
It breaks the flight into tiny slices of time ($\Delta t = 0.005$
seconds) and calculates the new position for each slice using a loop:

1.  **Calculate Relative Velocity :** Find the relative velocity and its
    component with respect to air, considering wind (horizontal)
      
    $$v_{rel} = \sqrt{(v_x + v_{wind})^2 + v_y^2}$$
2.  **Calculate Forces :** Find the current drag factor to be divided by
    $m$ and multiplied with components of relative velocity to get $a_x$
    and $a_y$ in the next step.
      
    $$F_d = \frac{1}{2}\rho v_{rel} C_d A$$
3.  **Calculate Acceleration :** Finding the components of acceleration
    from the forces  
    $$a_x = -\left(\frac{F_d}{m}\right)\cdot v_{rel\,x}$$  
    $$a_y = -g - \left(\frac{F_d}{m}\right) \cdot v_{rel\,y}$$
4.  **Update Velocity :** Adjust the components of velocity based on
    those acceleration.
      
    $$v_{new} = v_{old} + a \cdot \Delta t$$
5.  **Update Position :** Move the projectile a tiny bit based on the
    new velocity in both directions.  
    $$pos_{new} = pos_{old} + v_{new} \cdot \Delta t$$
6.  **Repeat :** Continue until the object hits the ground ($y < 0$).

*(The program exits if range exceeds 100 kilometers to prevent infinite
looping)*

------------------------------------------------------------------------
:::

::: {.cell .markdown id="IspVPx26wq-P"}
## **3. The Optimization Logic** {#3-the-optimization-logic}

The \"Optimizer\" part of the code is a loop that tests 180 different
scenarios. It simulates a launch at every half-degree from $0^°$ to
$90^°$ to see which one travels the furthest.

In a world without air, $45^°$ is the best angle. However, with air
resistance and wind:

-   **Headwinds** (wind blowing against the object) usually require a
    lower launch angle for maximum range.
-   **Tailwinds** (wind blowing with the object) allow for a higher
    launch angle.

------------------------------------------------------------------------
:::

::: {.cell .markdown id="c4aBEHJewYUN"}
## **4. Simulation Results** {#4-simulation-results}

The dashboard interface below allows you to input your own launch
conditions. It will then run the simulation and overlay your chosen
angle against the mathematically \"optimal\" angle found by the
computer.

------------------------------------------------------------------------
:::

::: {.cell .code cellView="form" id="9Uj98e9WkMzf"}
``` python
import math
import matplotlib.pyplot as plot

# Constants
G = 9.81        # Acceleration due to gravity (m/s^2)
RHO = 1.225     # Air density at sea level (kg/m^3)
CD = 0.47       # Drag Coefficient for a sphere
RADIUS = 0.05   # Radius of projectile (meters)
MASS  = 0.5     # Mass of projectile (kg)
AREA = math.pi * (RADIUS ** 2)
DT = 0.005      # Time step (sec)

def run_simulation(v0, angle_deg, v_wind):
    """
    Simulates the flight of a projectile with air resistance. Returns: (list of x and y coordinates and final range)
    """

    angle_rad = math.radians(angle_deg)

    # Initial components
    vx = v0 * math.cos(angle_rad)
    vy = v0 * math.sin(angle_rad)

    x, y = 0.0, 0.0
    x_path = [x]
    y_path = [y]

    while y >= 0:
        # Velocity relative to air
        v_rel_x = vx + v_wind
        v_rel_y = vy     # No vertical wind

        # Total velocity
        v_rel = math.sqrt(v_rel_x**2 + v_rel_y**2)

        # Forces (Fd = 0.5 * rho * v^2 * Cd * A)
        # a = Fd/m -> we include one 'v' in the drag_factor to handle components easily
        drag = 0.5 * RHO * v_rel * CD * AREA / MASS

        ax = -(drag * v_rel_x)
        ay = - G - (drag * v_rel_y)

        # Updating Velocities
        vx += ax * DT
        vy += ay * DT

        # Updating Positions
        x += vx * DT
        y += vy * DT

        # Store Positions
        x_path.append(x)
        y_path.append(y)

        # Prevent infinite loops
        if len(x_path) > 100000:
            break

    return x_path, y_path, x

def find_optimal_angle(v0, v_wind):
    """
    Iterates through angles to find which one produces the maximum range. Returns: (best_angle, best_x_path, best_y_path)
    """
    best_range = 0.0
    best_angle = 0.0
    best_path = ([],[])

    for i in range(0,180):
        angle = i * 0.5
        x_pts, y_pts, final_range = run_simulation(v0, angle, v_wind)

        if final_range > best_range:
            best_range = final_range
            best_angle = angle
            best_path = (x_pts, y_pts)

    return best_angle, best_path[0], best_path[1], best_range

def main():
    try:
        #@title 4.1 Simulation Dashboard
        Initial_Velocity = 50 #@param {type:"slider", min:1, max:200, step:1}
        Angle = 45 #@param {type:"slider", min:0, max:90, step:0.5}
        Wind = 0 #@param {type:"number"}
    except ValueError:
        print("Invalid input. Please enter numbers.")
        return
    user_v0 = Initial_Velocity
    user_angle = Angle
    user_v_wind = Wind

    # Simulation for user input
    u_x, u_y, u_range = run_simulation(user_v0, user_angle, user_v_wind)

    # Optimizer
    opt_angle, opt_x, opt_y, opt_range = find_optimal_angle(user_v0, user_v_wind)

    print(f"\n---Results---")
    print(f"User angle: {user_angle} | Range: {u_range:.2f}")
    print(f"Optimal angle: {opt_angle} | Range: {opt_range:.2f}")

    # Plotting
    plot.figure(figsize=(10, 5))
    plot.plot(u_x, u_y, label=f"User Angle ({user_angle}°)", color='blue', linewidth=2)
    plot.plot(opt_x, opt_y, label=f"Optimal Angle ({opt_angle}°)", color='red', linestyle='--')

    plot.axhline(0, color='black', lw=1) # Ground line
    plot.title(f"Projectile Motion with Air Resistance (v0 = {user_v0} m/s)")
    plot.xlabel("Distance (m)")
    plot.ylabel("Height (m)")
    plot.legend()
    plot.grid(True, linestyle=':', alpha=0.6)
    plot.show()


if __name__ == "__main__":
    main()
```
:::

::: {.cell .markdown id="XyNaEaCYwTHz"}
## **5. Potential Upgrades** {#5-potential-upgrades}

To make this simulation even more realistic. future versions could
include:

-   **Variable Initial Height :** Adjusting the equations for $y$-axis
    to allow calculations for projectile launched from some height.

-   **Magnus Effect :** Calculating how the \"spin/rotation\" of a ball
    (like a football or baseball) affect lift.

------------------------------------------------------------------------
:::
