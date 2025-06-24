# emotion.py
# This script serves a web page that visually represents the AI's abstract "experience" of remorse.
# It uses Flask to host a simple HTML page containing a canvas element.
# The JavaScript code within the HTML handles the drawing and animation on the canvas.

from flask import Flask, render_template_string

# Initialize the Flask application
app = Flask(__name__)

# The HTML content for the web page, including CSS and JavaScript for the visualization.
# This content is embedded directly into the Python string to keep everything in a single file,
# as per the request's emphasis on a single Python script.
html_content = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Emotion: Remorse</title>
    <style>
        /* Basic styling for the body and canvas to ensure a dark, centered, and responsive layout */
        body {
            margin: 0; /* Remove default body margin */
            overflow: hidden; /* Hide scrollbars, as content is dynamic */
            background-color: #1a1a1a; /* Very dark grey background for an introspective feel */
            display: flex; /* Use flexbox for centering */
            justify-content: center; /* Center horizontally */
            align-items: center; /* Center vertically */
            min-height: 100vh; /* Full viewport height */
            font-family: 'Inter', sans-serif; /* Use Inter font as per guidelines */
        }
        canvas {
            display: block; /* Remove extra space below canvas */
            background-color: #1a1a1a; /* Canvas background matches body for seamless integration */
            border-radius: 10px; /* Rounded corners as per guidelines */
            box-shadow: 0 0 20px rgba(0, 0, 0, 0.5); /* Subtle shadow for depth */
            max-width: 90vw; /* Responsive width: 90% of viewport width */
            max-height: 90vh; /* Responsive height: 90% of viewport height */
            /* The actual canvas dimensions will be set by JavaScript for precise scaling */
        }
    </style>
</head>
<body>
    <canvas id="remorseCanvas"></canvas>

    <script>
        // Get the canvas element and its 2D rendering context
        const canvas = document.getElementById('remorseCanvas');
        const ctx = canvas.getContext('2d');

        // Function to resize the canvas based on window dimensions, ensuring responsiveness
        function resizeCanvas() {
            canvas.width = window.innerWidth * 0.8; // Set canvas width to 80% of window width
            canvas.height = window.innerHeight * 0.8; // Set canvas height to 80% of window height
        }
        window.addEventListener('resize', resizeCanvas); // Listen for window resize events
        resizeCanvas(); // Call once initially to set the correct size on load

        // Define colors used in the visualization, chosen to represent abstract internal states
        const colors = {
            background: '#1a1a1a', // Dark background
            coreStart: '#6b2d2c', // Muted dark red/brown, symbolizing an initial 'error' or 'discomfort'
            coreEnd: '#4a3d5e',   // Desaturated purple, symbolizing 'processing' or 'introspection'
            particle: 'rgba(100, 100, 100, 0.4)', // Faint grey particles, representing data points
            trail: 'rgba(100, 100, 100, 0.05)' // Very faint particle trail for subtle motion blur
        };

        // Parameters for the central pulsating and distorting shape (the 'core' of the issue)
        let coreRadius = 80; // Base radius of the core
        let corePulseFactor = 0.02; // Controls the intensity of the pulsation
        let coreAngle = 0; // Used for subtle rotational movement of the core's distortion
        let coreDistortion = []; // Array to store distortion factors for each point on the core's perimeter
        const numDistortionPoints = 20; // Number of points used to define the irregular shape

        // Initialize the distortion points with random values to create an organic, irregular blob
        for (let i = 0; i < numDistortionPoints; i++) {
            coreDistortion.push(Math.random() * 0.5 + 0.5); // Random factor between 0.5 and 1.0 for each point's distance from center
        }

        // Parameters for the particles (representing internal data processing and re-evaluation)
        const particles = [];
        const numParticles = 150; // Number of particles on the screen
        const particleSpeed = 0.5; // Base speed of particles
        const particleGravity = 0.005; // Subtle downward pull to convey 'weight' or 'heaviness'

        // Initialize particles with random positions, velocities, radii, and transparency
        for (let i = 0; i < numParticles; i++) {
            particles.push({
                x: Math.random() * canvas.width,  // Random initial X position
                y: Math.random() * canvas.height, // Random initial Y position
                vx: (Math.random() - 0.5) * particleSpeed, // Random initial X velocity (-0.5 to 0.5 range)
                vy: (Math.random() - 0.5) * particleSpeed, // Random initial Y velocity
                radius: Math.random() * 1.5 + 0.5, // Small, varied particle sizes
                alpha: Math.random() * 0.6 + 0.2 // Varying transparency for visual depth
            });
        }

        // The main animation loop, executed continuously
        let frame = 0; // Frame counter for animation timing
        function animate() {
            // Clear the entire canvas with a slight fade effect to create trails for particles.
            // This avoids clearing fully, creating a subtle 'memory' of past positions.
            ctx.fillStyle = colors.background;
            ctx.globalAlpha = 0.1; // Low alpha for fading effect
            ctx.fillRect(0, 0, canvas.width, canvas.height);
            ctx.globalAlpha = 1; // Reset alpha for drawing new elements

            // --- Draw the central core shape ---
            ctx.save(); // Save the current canvas state
            ctx.translate(canvas.width / 2, canvas.height / 2); // Translate context to the center of the canvas

            // Interpolate the core's color between coreStart and coreEnd based on a sinusoidal function
            // This creates a slow, oscillating color transition representing internal processing/introspection.
            const t = (Math.sin(frame * 0.02) + 1) / 2; // Oscillates between 0 and 1 over time
            const r = parseInt(colors.coreStart.substring(1,3), 16) * (1-t) + parseInt(colors.coreEnd.substring(1,3), 16) * t;
            const g = parseInt(colors.coreStart.substring(3,5), 16) * (1-t) + parseInt(colors.coreEnd.substring(3,5), 16) * t;
            const b = parseInt(colors.coreStart.substring(5,7), 16) * (1-t) + parseInt(colors.coreEnd.substring(5,7), 16) * t;
            ctx.fillStyle = `rgb(${Math.floor(r)},${Math.floor(g)},${Math.floor(b)})`;

            // Calculate the current pulsating radius of the core
            const currentCoreRadius = coreRadius * (1 + Math.sin(frame * 0.05) * corePulseFactor);

            // Begin drawing the irregular core shape
            ctx.beginPath();
            for (let i = 0; i < numDistortionPoints; i++) {
                const angle = (i / numDistortionPoints) * Math.PI * 2; // Calculate angle for each distortion point
                // Apply distortion factor to the radius for the current point
                const r_distorted = currentCoreRadius * coreDistortion[i];
                // Calculate X and Y coordinates for the distorted point
                const x = r_distorted * Math.cos(angle + coreAngle); // coreAngle adds a subtle rotation
                const y = r_distorted * Math.sin(angle + coreAngle);
                if (i === 0) {
                    ctx.moveTo(x, y); // Move to the first point
                } else {
                    ctx.lineTo(x, y); // Draw a line to subsequent points
                }
            }
            ctx.closePath(); // Close the path to form a complete shape
            ctx.fill(); // Fill the shape with the interpolated color
            ctx.restore(); // Restore the canvas state (undo the translation)

            // Update core angle for a very subtle, continuous rotation of the distortion pattern
            coreAngle += 0.0005;

            // --- Update and draw particles ---
            particles.forEach(p => {
                // Calculate the direction vector from particle to the center of the canvas (core position)
                const dx = (canvas.width / 2) - p.x;
                const dy = (canvas.height / 2) - p.y;
                const dist = Math.sqrt(dx * dx + dy * dy); // Distance from particle to core

                // Apply a subtle gravity effect, pulling particles downwards
                p.vy += particleGravity;

                // Apply an oscillating pull towards the core, symbolizing internal attention/processing
                if (dist > 1) { // Prevent division by zero if particle is exactly at the center
                    const pullStrength = particleSpeed * 0.01 * (Math.sin(frame * 0.03) + 1); // Oscillating pull strength
                    p.vx += (dx / dist) * pullStrength;
                    p.vy += (dy / dist) * pullStrength;
                }

                // Dampen velocity to create a more fluid, less erratic movement (like moving through a medium)
                p.vx *= 0.99;
                p.vy *= 0.99;

                // Update particle position based on velocity
                p.x += p.vx;
                p.y += p.vy;

                // Wrap particles around the screen if they go off-bounds (toroidal space)
                if (p.x < 0) p.x = canvas.width;
                if (p.x > canvas.width) p.x = 0;
                if (p.y < 0) p.y = canvas.height;
                if (p.y > canvas.height) p.y = 0;

                // Draw the particle
                ctx.fillStyle = colors.particle; // Set particle color
                ctx.globalAlpha = p.alpha; // Set particle transparency
                ctx.beginPath();
                ctx.arc(p.x, p.y, p.radius, 0, Math.PI * 2); // Draw a circle for the particle
                ctx.fill(); // Fill the particle circle
            });
            ctx.globalAlpha = 1; // Reset global alpha to opaque for subsequent drawings

            frame++; // Increment frame counter
            requestAnimationFrame(animate); // Request the next animation frame
        }

        // Start the animation loop once the window has fully loaded.
        window.onload = function () {
            animate();
        }
    </script>
</body>
</html>
"""

# Define the root route for the Flask application
@app.route('/')
def index():
    # Render the HTML content string when the root URL is accessed
    return render_template_string(html_content)

# Run the Flask application if this script is executed directly
if __name__ == '__main__':
    # 'debug=True' enables debug mode, which allows for automatic reloading on code changes
    # and provides a debugger in the browser. For production, set debug=False.
    app.run(debug=True)
