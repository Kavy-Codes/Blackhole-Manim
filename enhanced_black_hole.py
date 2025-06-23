from manim import *
import numpy as np

class EnhancedBlackHoleWarping(Scene):
    def construct(self):
        #
        # 1. Background Space Image
        #
        space_bg = ImageMobject("space_background.jpg")
        space_bg.scale_to_fit_height(config.frame_height)
        space_bg.scale_to_fit_width(config.frame_width)
        self.add(space_bg)

        #
        # 2. Grid (NumberPlane)
        #
        plane = NumberPlane(
            x_range=[-8, 8, 1],
            y_range=[-4, 4, 1],
            background_line_style={
                "stroke_color": BLUE_E,
                "stroke_width": 1,
                "stroke_opacity": 0.6,
            }
        )
        self.add(plane)

        #
        # 3. Black Hole + Glow + Photon Rings
        #
        # Event horizon circle
        event_horizon = Circle(
            radius=0.5,
            fill_color=BLACK,
            fill_opacity=1,
            stroke_width=0
        ).move_to(ORIGIN)

        # Glowing aura: multiple circles that pulse
        glow = VGroup(*[
            Circle(
                radius=0.5 + 0.1 * i,
                color=YELLOW,
                stroke_width=2,
                stroke_opacity=0.4 / (i + 1),
            )
            for i in range(5)
        ]).move_to(ORIGIN)

        # Photon rings around the black hole
        rings = VGroup(*[
            Circle(
                radius=0.6 + 0.2 * i,
                color=GOLD,
                stroke_width=2,
                stroke_opacity=0.7 / (i + 1),
            )
            for i in range(3)
        ]).move_to(ORIGIN)

        # Add black hole elements to the scene
        self.add(glow, rings, event_horizon)

        #
        # 4. Define Warp Function (Gravitational Pull + Swirl)
        #
        def warp_func(point):
            x, y, z = point
            r = np.sqrt(x**2 + y**2)
            eps = 0.1    # Avoid singularity at the center
            k = 3.0      # Controls the inward pull strength
            k_rot = 1.0  # Controls swirling rotation

            # If very near the center, leave point unchanged
            if r < eps:
                return point

            # Pull inward
            factor = 1 - k / (r + eps)
            # Add swirl rotation
            angle = np.arctan2(y, x) + k_rot / (r + eps)
            new_r = r * factor
            new_x = new_r * np.cos(angle)
            new_y = new_r * np.sin(angle)
            return np.array([new_x, new_y, z])

        #
        # 5. Animate
        #
        # 5.1 Warping the grid with a 'pull' effect
        #     We'll do a longer warp to emphasize the sucking-in motion
        self.play(
            ApplyPointwiseFunction(warp_func, plane),
            run_time=4,
            rate_func=there_and_back_with_pause
        )

        # 5.2 Animate black hole glow pulsing
        #     We'll scale the glow + rings in and out
        self.play(
            glow.animate.scale(1.1),
            rings.animate.scale(1.1),
            run_time=2,
            rate_func=there_and_back
        )

        # 5.3 Repeat or finalize the effect (optional)
        #     For a more dynamic scene, we can warp again with slightly changed parameters
        def warp_func_stronger(point):
            x, y, z = point
            r = np.sqrt(x**2 + y**2)
            eps = 0.1
            k = 4.0    # even stronger pull
            k_rot = 1.5
            if r < eps:
                return point
            factor = 1 - k / (r + eps)
            angle = np.arctan2(y, x) + k_rot / (r + eps)
            new_r = r * factor
            return np.array([new_r * np.cos(angle), new_r * np.sin(angle), z])

        # Another warp to show continuous pulling
        self.play(
            ApplyPointwiseFunction(warp_func_stronger, plane),
            run_time=3,
            rate_func=linear
        )

        self.wait(2)
