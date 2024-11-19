#include <SDL2/SDL.h>
#include <iostream>

const int WIDTH = 800;
const int HEIGHT = 600;


int selectOption(int option){
	const int tam = 2;

	const std::string options[tam] = {
		"1 - Draw Mode",
		"2 - Colicionar"
	};

	for (int i = 0; i < tam; i++){
		std::cout << options[i] << std::endl;
	}
	
	std::cout << ">";	
	std::cin >> option;
	std::cout << std::endl;

	return option;
}

int main(int argc, char* argv[]) {
	
	std::cout << "P para ver las opciones" << std::endl;
	
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


	int option;
	bool running = true;
	bool click = false;
	

	float puntoMedioX = WIDTH / 2;
	float puntoAltoY = HEIGHT;

	SDL_Event event;
	SDL_RenderPresent(renderer); 	
	// Bucle principal
	while (running) {
		SDL_SetRenderDrawColor(renderer, 255, 255, 255, 255);


		SDL_RenderDrawLine(renderer, puntoMedioX, puntoAltoY, puntoMedioX, 0);


			
		// Procesar eventos
		while (SDL_PollEvent(&event)) {
			if (event.type == SDL_QUIT) {
				running = false;
			}
			else if (event.type == SDL_MOUSEBUTTONDOWN && event.button.button == SDL_BUTTON_LEFT) {
				click = true;  // Empezar a dibujar
			}
			else if (event.type == SDL_MOUSEBUTTONUP && event.button.button == SDL_BUTTON_LEFT) {
				click = false;  // Detener el dibujo
			}

			else if (event.type == SDL_KEYDOWN && event.key.keysym.sym == SDLK_ESCAPE){
			

				running = false;
			}
			else if (event.type == SDL_KEYDOWN && event.key.keysym.sym == SDLK_p){
				option = selectOption(option); 			
			}

		}


		int mouseX, mouseY;


		// Dibujar si se mantiene presionado el botón izquierdo
		if (click == true && option == 1) {
			SDL_GetMouseState(&mouseX, &mouseY);

			// Establecer color de dibujo (negro) y dibujar el punto
			SDL_SetRenderDrawColor(renderer, 217, 237, 146, SDL_ALPHA_OPAQUE);
			
			int am = 10;

			//SDL_RenderDrawPoint(renderer, mouseX, mouseY);
			for(int a = 0; a < 10; a++) {
				SDL_RenderDrawPoint(renderer, mouseX + a, mouseY + a);
				SDL_RenderDrawPoint(renderer, mouseX - a, mouseY - a);
				SDL_RenderDrawPoint(renderer, mouseX + a, mouseY - a);
				SDL_RenderDrawPoint(renderer, mouseX - a, mouseY + a);
				SDL_RenderDrawPoint(renderer, mouseX - a, mouseY);
				SDL_RenderDrawPoint(renderer, mouseX + a, mouseY);
				SDL_RenderDrawPoint(renderer, mouseX, mouseY + a);
				SDL_RenderDrawPoint(renderer, mouseX, mouseY - a);
			}	
			SDL_RenderPresent(renderer);  // Actualizar pantalla en cada punto dibujado
		}

		

		if(option == 2){
			


		}
		

		SDL_RenderPresent(renderer);

		//SDL_Delay(1);  // Reducir uso de CPU
	}

	// Limpiar y cerrar
	SDL_DestroyRenderer(renderer);
	SDL_DestroyWindow(window);
	SDL_Quit();

	return 0;
}
