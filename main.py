import sys
from modules.wind import Wind
from modules.layer import Layer
from modules.constants import *


def main():
    """
    Main function to run the snowfall simulation.
    """
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Snowfall Simulation")
    clock = pygame.time.Clock()

    layers = []
    for index, amount in dict_layer_to_amount.items():
        # Create layers based on the dict_layer_to_amount dictionary
        new_layer = Layer(distance=layers_count - index + 1,
                          mass=index,
                          snowflakes_count=amount,
                          wind=Wind(),
                          color_scale=index / layers_count)
        layers.append(new_layer)

    global_wind = Wind()  # Create a global wind affecting all layers

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        global_wind.cyclic_update(cycle=10, min_wind=0)  # Update global wind cyclically

        # Clear the screen and draw the gradient background
        gradient_background = create_gradient_surface(WIDTH, HEIGHT, DARK_BLUE, LIGHT_BLUE)
        screen.blit(gradient_background, (0, 0))

        for layer in layers:
            layer.wind.cyclic_update(cycle=layer.mass)  # Update wind for each layer cyclically
            layer.apply_wind(layer.wind.add(global_wind.scale(2)))  # Apply wind effects
            layer.update()  # Update snowflake positions in the layer
            layer.draw(screen)  # Draw the layer

        # Update the display
        pygame.display.flip()
        clock.tick(60)


if __name__ == "__main__":
    main()
