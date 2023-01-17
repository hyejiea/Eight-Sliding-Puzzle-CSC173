import pygame
import pygame_gui

# local imports
import main as m


# width and height are not final and are subject to change as UI changes
WINDOW_WIDTH = 900
WINDOW_HEIGHT = 750
TILE_AREA_WIDTH = 600
TILE_AREA_HEIGHT = 600
TILE_WIDTH = TILE_AREA_WIDTH / 3
TILE_HEIGHT = TILE_AREA_HEIGHT / 3
BUTTON_AREA_WIDTH = WINDOW_WIDTH - TILE_AREA_WIDTH
BUTTON_WIDTH = 240
BUTTON_HEIGHT = 80
BUTTON_MARGIN = (BUTTON_AREA_WIDTH - BUTTON_WIDTH) // 2
CENTER_X = 300
CENTER_Y = 300
LABEL_WIDTH = 640
LABEL_HEIGHT = 500
WAIT_TIME = 1000

# colors
GREEN = (0, 204, 0)
BLUE = (0, 0, 204)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
DARKTURQUOISE = (3, 54, 73)


BACKGROUND_COLOR = BLACK

BASICFONTSIZE = 60

APPLICATION_TITLE = "8-Puzzle"

ALERTLABELEVENT = pygame.USEREVENT + 2


pygame.init()


BASICFONT = pygame.font.SysFont('fonts/consola.ttf', BASICFONTSIZE)
BUTTON_FONT = pygame.font.SysFont('fonts/consola.ttf', BASICFONTSIZE // 2)


window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))


manager = pygame_gui.UIManager((WINDOW_WIDTH, WINDOW_HEIGHT))


pygame.display.set_caption(APPLICATION_TITLE)


class Tile:

    def __init__(self, number, tile_width, tile_height, index_x, index_y):
        self.number = number
        self.x = 0
        self.y = 0
        self.width = tile_width
        self.height = tile_height
        self.index_x = index_x
        self.index_y = index_y


    def tileStats(self):
        return self.x, self.y, self.width, self.height




class ButtonRect:

    def __init__(self, id, ):
        self.Rect = pygame.Rect(
            (WINDOW_WIDTH - BUTTON_AREA_WIDTH + BUTTON_MARGIN, id * BUTTON_HEIGHT + 10),  # left, top
            (BUTTON_WIDTH, BUTTON_HEIGHT))
        self.id = id


def alert_label(message):
    alertLabel.set_text(message)
    pygame.time.set_timer(ALERTLABELEVENT, WAIT_TIME)

def newState(state):

    gameState = m.GameState(None, None, state, 0)
    stateStr = str(gameState)


    initial_tiles_list = []

    blankTileLocal = Tile("0", TILE_WIDTH - 2, TILE_HEIGHT - 2, 0, 0)


    for i, num in enumerate(stateStr):


        index_x = (i // 3)
        index_y = (i % 3)


        if num != '0':

            tile = Tile(num, TILE_WIDTH - 2, TILE_HEIGHT - 2, index_x, index_y)

            tile.x = index_y * TILE_WIDTH + 1
            tile.y = index_x * TILE_HEIGHT + 1

            initial_tiles_list.append(tile)
        else:
            blankTileLocal.x = index_y * TILE_WIDTH + 1
            blankTileLocal.y = index_x * TILE_HEIGHT + 1
            blankTileLocal.index_x = index_x
            blankTileLocal.index_y = index_y
            initial_tiles_list.append(blankTileLocal)

    return gameState, initial_tiles_list, blankTileLocal



def updateBoard(direction):

    i, j = blankTile.index_x, blankTile.index_y
    list_index = 0


    if direction == 'Left':
        list_index = i * 3 + (j - 1)
    elif direction == 'Up':
        list_index = (i - 1) * 3 + j
    elif direction == 'Down':
        list_index = (i + 1) * 3 + j
    elif direction == 'Right':
        list_index = i * 3 + (j + 1)

    target_tile = numbered_tiles_list[list_index]
    blankTile_list_index = i * 3 + j

    target_tile.x, blankTile.x = blankTile.x, target_tile.x
    target_tile.y, blankTile.y = blankTile.y, target_tile.y
    target_tile.index_x, blankTile.index_x = blankTile.index_x, target_tile.index_x
    target_tile.index_y, blankTile.index_y = blankTile.index_y, target_tile.index_y

    numbered_tiles_list[list_index], numbered_tiles_list[blankTile_list_index] \
        = numbered_tiles_list[blankTile_list_index], numbered_tiles_list[list_index]



def swapTiles(mousePosition):
    x, y = mousePosition
    index_y = x // TILE_WIDTH
    index_x = y // TILE_HEIGHT


    distance = abs(blankTile.index_x - index_x) + abs(blankTile.index_y - index_y)


    if distance == 1:
        if blankTile.index_y < index_y:  # blank tile will move right
            updateBoard("Right")
        elif blankTile.index_y > index_y:  # blank tile will move left
            updateBoard("Left")
        elif blankTile.index_x < index_x:
            updateBoard("Down")
        elif blankTile.index_x > index_x:
            updateBoard("Up")



randomStateButtonRect = ButtonRect(1)
randomStateButton = pygame_gui.elements.UIButton(
    relative_rect=randomStateButtonRect.Rect, text="Random Start", manager=manager
)


solveButtonRect = ButtonRect(3)
solveButton = pygame_gui.elements.UIButton(
    relative_rect=solveButtonRect.Rect, text="Solve", manager=manager
)

# slider to control speed of animation
speedSliderRect = ButtonRect(4)
speedSlider = pygame_gui.elements.UIHorizontalSlider(
    relative_rect=speedSliderRect.Rect, start_value=1, value_range=(1, 100),
    manager=manager
)

alertLabelRect = ButtonRect(5)
alertLabel = pygame_gui.elements.UILabel(
    relative_rect=alertLabelRect.Rect, manager=manager, text="Click Solve to solve!"
)

# Option box to select which searching algorithm to visualize
solveChoiceRect = ButtonRect(2)
solveChoice = pygame_gui.elements.UIDropDownMenu(
    ["BFS", "DFS", "A* Manhattan", "A* Euclid"], "BFS",
    relative_rect=solveChoiceRect.Rect, manager=manager)


initialState, numbered_tiles_list, blankTile = newState(12345678)


solutionExists = False


solutionStepsList = []
solutionIndex = 0

clock = pygame.time.Clock()

time_counter = 0
running = True
while running:

    time_delta = clock.tick(60) / 1000
    time_counter += time_delta * 1000



    if time_counter > 500 / speedSlider.get_current_value() and solutionExists:
        updateBoard(solutionStepsList[solutionIndex].move)
        time_counter = 0
        solutionIndex += 1
        if solutionIndex == len(solutionStepsList):
            solutionExists = False


            initialState, numbered_tiles_list, blankTile = newState(12345678)
            solutionStepsList = []


    events = pygame.event.get()


    for event in events:


        if event.type == pygame.USEREVENT:
            if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == randomStateButton:
                    state = m.random_game_state()
                    initialState, numbered_tiles_list, blankTile = newState(state)
                    solveButton.enable()
                    solutionExists = False
                elif event.ui_element == solveButton:
                    if initialState.state != m.goalState:
                        type_of_search = solveChoice.selected_option
                        answer = m.solve(initialState, type_of_search)
                        path_to_goal = m.iterative_get_path_(answer)
                        status = m.print_data(answer, type_of_search)
                        solveButton.disable()
                        if path_to_goal:
                            solutionExists = True
                            solutionIndex = 0
                            solutionStepsList = path_to_goal[1:]
                            alert_label("Solving...")
                        else:
                            alert_label("No solution!")
                            solveButton.enable()


                    else:
                        alert_label("Already solved")


        if event.type == ALERTLABELEVENT:
            alertLabel.set_text("")
            pygame.time.set_timer(ALERTLABELEVENT, 0)

        # Checking for a mouseclick on a tile
        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos

            if x < TILE_AREA_WIDTH and y < TILE_AREA_HEIGHT:
                pass


        if event.type == pygame.QUIT:
            running = False
            break

        manager.process_events(event)


    manager.update(time_delta)


    window.fill(BACKGROUND_COLOR)


    for tile in numbered_tiles_list:
        pygame.draw.rect(window, WHITE, tile.tileStats())


        textSurf = BASICFONT.render(tile.number, True, BLACK, WHITE)
        textRect = textSurf.get_rect()
        textRect.center = tile.x + TILE_WIDTH // 2, tile.y + TILE_HEIGHT // 2
        window.blit(textSurf, textRect)


    pygame.draw.rect(window, BACKGROUND_COLOR, blankTile.tileStats())


    manager.draw_ui(window)
    pygame.display.update()


pygame.quit()
