#include <SDL2/SDL.h>
#include <iostream>
#include <ctime> 
#include <string>

const int WIDTH = 800;
const int HEIGHT = 600;

int main(int argc, char* argv[]) {
    std::cout << "Presiona ESPACIO para iniciar." << std::endl;

    if (SDL_Init(SDL_INIT_VIDEO) != 0) {
        std::cerr << "Error al inicializar SDL: " << SDL_GetError() << std::endl;
        return 1;
    }

    SDL_Window* window = SDL_CreateWindow(
        "Simulacion",
        SDL_WINDOWPOS_CENTERED,
        SDL_WINDOWPOS_CENTERED,
        WIDTH, HEIGHT,
        SDL_WINDOW_SHOWN
    );
    if (!window) {
        std::cerr << "Error al crear la ventana: " << SDL_GetError() << std::endl;
        SDL_Quit();
        return 1;
    }

    SDL_Renderer* renderer = SDL_CreateRenderer(window, -1, SDL_RENDERER_ACCELERATED);
    if (!renderer) {
        std::cerr << "Error al crear el renderer: " << SDL_GetError() << std::endl;
        SDL_DestroyWindow(window);
        SDL_Quit();
        return 1;
    }

    SDL_SetRenderDrawColor(renderer, 52, 160, 164, SDL_ALPHA_OPAQUE);
    SDL_RenderClear(renderer);


    /*
    SDL_SetRenderDrawColor(renderer, 255, 255, 255, SDL_ALPHA_OPAQUE);
    SDL_RenderDrawLine(renderer, WIDTH / 2, HEIGHT, WIDTH / 2, 0);
    SDL_RenderPresent(renderer);
    */

    bool running = true;
	bool start = false;
    SDL_Event event;


	int mapa[HEIGHT][WIDTH];

    while (running) {
        
		while (SDL_PollEvent(&event)) {

            if (event.type == SDL_QUIT) {
                running = false;
            }

            if (event.type == SDL_KEYDOWN && event.key.keysym.sym == SDLK_SPACE) {
                start = true;
            }
			
            if (event.type == SDL_KEYDOWN && event.key.keysym.sym == SDLK_ESCAPE) {
                running = false;
            }

        }

        if (start) {
           for(int i = 0; i < HEIGHT - 100; i++){
				
				for(int a = 0; a < WIDTH - 100; a++){
						
					bool add = false;
					int probavilidad = 1;


					int prob = rand() % probavilidad;

					if (probavilidad <= 1){
						add = true;
					}

					if (add){
						mapa[i][a] = 1;	
					}

				}
			
			}

			for(int i = 0; i < HEIGHT; i++){
				for(int a = 0; a < WIDTH; a++){
					if(mapa[i][a] == 1){
                        SDL_SetRenderDrawColor(renderer, 217, 237, 146, SDL_ALPHA_OPAQUE);
						SDL_RenderDrawPoint(renderer, i, a);
					}
				}
			}

        }

        SDL_RenderPresent(renderer);
    }

    SDL_DestroyRenderer(renderer);
    SDL_DestroyWindow(window);
    SDL_Quit();
    return 0;
}
/*
for(int i = 0; i < HEIGHT; i++){
				
				for(int a = 0; a < WIDTH; a++){
						
					bool add = false;
					int probavilidad = 1;


					if (a > 100 || i > 100){
						probavilidad = 1;
					}

					int prob = rand() % probavilidad;

					if (probavilidad <= 1){
						add = true;
					}

					if (add){
						
					}

				}
			
			}
*/