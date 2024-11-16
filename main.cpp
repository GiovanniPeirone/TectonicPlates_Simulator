#include <SDL2/SDL.h>
#include <iostream>

const int WIDTH = 800;
const int HEIGHT = 600;

/*
SDL_Renderer dibujar(SDL_Renderer renderer,int mouseX,int mouseY) {
    SDL_RenderDrawPoint(renderer, mouseX, mouseY - 1);
    SDL_RenderDrawPoint(renderer, mouseX - 1, mouseY);
    SDL_RenderDrawPoint(renderer, mouseX, mouseY);
    SDL_RenderDrawPoint(renderer, mouseX + 1, mouseY);
    SDL_RenderDrawPoint(renderer, mouseX, mouseY + 1);

}
*/
int main(int argc, char* argv[]) {
	// Inicializar SDL
	if (SDL_Init(SDL_INIT_EVERYTHING) != 0) {
		std::cerr << "Error al inicializar SDL: " << SDL_GetError() << std::endl;
		return 1;
	}

	// Crear la ventana
	SDL_Window* window = SDL_CreateWindow(  
			"Dibuja con el ratón",
			SDL_WINDOWPOS_CENTERED,
			SDL_WINDOWPOS_CENTERED,
			WIDTH, HEIGHT,
			SDL_WINDOW_SHOWN);

	if (!window) {
		std::cerr << "Error al crear la ventana: " << SDL_GetError() << std::endl;
		SDL_Quit();
		return 1;
	}
	
	// Crear el renderer
	SDL_Renderer* renderer = SDL_CreateRenderer(window, -1, SDL_RENDERER_ACCELERATED);
	if (!renderer) {
		std::cerr << "Error al crear el renderer: " << SDL_GetError() << std::endl;
		SDL_DestroyWindow(window);
		SDL_Quit();
		return 1;
	}

	// Establecer color de fondo (blanco) y limpiar
	SDL_SetRenderDrawColor(renderer, 52, 160, 164, SDL_ALPHA_OPAQUE);	
	SDL_RenderClear(renderer);



	bool running = true;
	bool drawing = false;
	

	SDL_Event event;
	SDL_RenderPresent(renderer); 	
	// Bucle principal
	while (running) {
		// Procesar eventos
		while (SDL_PollEvent(&event)) {
			if (event.type == SDL_QUIT) {
				running = false;
			}
			else if (event.type == SDL_MOUSEBUTTONDOWN && event.button.button == SDL_BUTTON_LEFT) {
				drawing = true;  // Empezar a dibujar
			}
			else if (event.type == SDL_MOUSEBUTTONUP && event.button.button == SDL_BUTTON_LEFT) {
				drawing = false;  // Detener el dibujo
			}

			else if (event.type == SDL_KEYDOWN && event.key.keysym.sym == SDLK_ESCAPE){
			

				running = false;
			}

			else if ()
		}

		// Dibujar si se mantiene presionado el botón izquierdo
		if (drawing == true) {
			int mouseX, mouseY;
			SDL_GetMouseState(&mouseX, &mouseY);

			// Establecer color de dibujo (negro) y dibujar el punto
			SDL_SetRenderDrawColor(renderer, 217, 237, 146, SDL_ALPHA_OPAQUE);
			
			int am = 10;

			//SDL_RenderDrawPoint(renderer, mouseX, mouseY);
			for(int a = 0; a < 10; a++) {
				SDL_RenderDrawPoint(renderer, mouseX + a, mouseY + a);
				SDL_RenderDrawPoint(renderer, mouseX - a, mouseY - a);
			}	
			SDL_RenderPresent(renderer);  // Actualizar pantalla en cada punto dibujado
		






		}

		SDL_Delay(1);  // Reducir uso de CPU
	}

	// Limpiar y cerrar
	SDL_DestroyRenderer(renderer);
	SDL_DestroyWindow(window);
	SDL_Quit();

	return 0;
}
