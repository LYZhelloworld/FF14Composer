import pygame
import pygame.midi


class Composer:
    VELOCITY = 127
    INSTRUMENT = 46  # Harp
    # INSTRUMENT = 0 # Grand piano
    # INSTRUMENT = 25 # Steel guitar
    # INSTRUMENT = 45 # Pizzicato
    # INSTRUMENT = 73 # Flute
    # INSTRUMENT = 68 # Oboe
    # INSTRUMENT = 71 # Clarinet
    # INSTRUMENT = 72 # Piccolo

    NOTE_C_MIDDLE = 72

    NOTE_C = NOTE_C_MIDDLE
    NOTE_C_SHARP = NOTE_C_MIDDLE + 1
    NOTE_D = NOTE_C_MIDDLE + 2
    NOTE_D_SHARP = NOTE_C_MIDDLE + 3
    NOTE_E = NOTE_C_MIDDLE + 4
    NOTE_F = NOTE_C_MIDDLE + 5
    NOTE_F_SHARP = NOTE_C_MIDDLE + 6
    NOTE_G = NOTE_C_MIDDLE + 7
    NOTE_G_SHARP = NOTE_C_MIDDLE + 8
    NOTE_A = NOTE_C_MIDDLE + 9
    NOTE_A_SHARP = NOTE_C_MIDDLE + 10
    NOTE_B = NOTE_C_MIDDLE + 11
    NOTE_C_OCTAVE = NOTE_C_MIDDLE + 12

    key_bindings = {
        pygame.K_z: NOTE_C,
        pygame.K_x: NOTE_D,
        pygame.K_c: NOTE_E,
        pygame.K_v: NOTE_F,
        pygame.K_b: NOTE_G,
        pygame.K_n: NOTE_A,
        pygame.K_m: NOTE_B,
        pygame.K_COMMA: NOTE_C_OCTAVE,
        pygame.K_s: NOTE_C_SHARP,
        pygame.K_d: NOTE_D_SHARP,
        pygame.K_g: NOTE_F_SHARP,
        pygame.K_h: NOTE_G_SHARP,
        pygame.K_j: NOTE_A_SHARP
    }

    def __init__(self):
        self.current_note = None
        self.stat_shift = False
        self.stat_ctrl = False
        self.stat_key = None
        pygame.midi.init()
        self.player = pygame.midi.Output(0)
        self.player.set_instrument(Composer.INSTRUMENT)

    def close(self):
        del self.player
        pygame.midi.quit()

    def play(self):
        if self.current_note:
            self.player.note_on(self.current_note, Composer.VELOCITY)

    def end(self):
        if self.current_note:
            self.player.note_off(self.current_note, Composer.VELOCITY)

    def process_input(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key in Composer.key_bindings:
                self.stat_key = event.key
        elif event.type == pygame.KEYUP:
            if event.key in Composer.key_bindings:
                if event.key == self.stat_key:
                    self.stat_key = None
        mods = pygame.key.get_mods()
        new_note = self.calc_note(
            self.stat_key, mods & pygame.KMOD_SHIFT, mods & pygame.KMOD_CTRL)
        if new_note != self.current_note:
            self.end()
            self.current_note = new_note
            self.play()

    def calc_note(self, key, shift, ctrl):
        if key in Composer.key_bindings:
            new_note = Composer.key_bindings[key]
            if shift:
                new_note += 12
            elif ctrl:
                new_note -= 12
            return new_note
        else:
            return None


NOTE_NAME = {
    Composer.NOTE_C: 'C',
    Composer.NOTE_D: 'D',
    Composer.NOTE_E: 'E',
    Composer.NOTE_F: 'F',
    Composer.NOTE_G: 'G',
    Composer.NOTE_A: 'A',
    Composer.NOTE_B: 'B',
    Composer.NOTE_C_SHARP: 'C#',
    Composer.NOTE_D_SHARP: 'D#',
    Composer.NOTE_F_SHARP: 'F#',
    Composer.NOTE_G_SHARP: 'G#',
    Composer.NOTE_A_SHARP: 'A#',
    Composer.NOTE_C + 12: 'C+',
    Composer.NOTE_D + 12: 'D+',
    Composer.NOTE_E + 12: 'E+',
    Composer.NOTE_F + 12: 'F+',
    Composer.NOTE_G + 12: 'G+',
    Composer.NOTE_A + 12: 'A+',
    Composer.NOTE_B + 12: 'B+',
    Composer.NOTE_C_SHARP + 12: 'C#+',
    Composer.NOTE_D_SHARP + 12: 'D#+',
    Composer.NOTE_F_SHARP + 12: 'F#+',
    Composer.NOTE_G_SHARP + 12: 'G#+',
    Composer.NOTE_A_SHARP + 12: 'A#+',
    Composer.NOTE_C - 12: 'C-',
    Composer.NOTE_D - 12: 'D-',
    Composer.NOTE_E - 12: 'E-',
    Composer.NOTE_F - 12: 'F-',
    Composer.NOTE_G - 12: 'G-',
    Composer.NOTE_A - 12: 'A-',
    Composer.NOTE_B - 12: 'B-',
    Composer.NOTE_C_SHARP - 12: 'C#-',
    Composer.NOTE_D_SHARP - 12: 'D#-',
    Composer.NOTE_F_SHARP - 12: 'F#-',
    Composer.NOTE_G_SHARP - 12: 'G#-',
    Composer.NOTE_A_SHARP - 12: 'A#-',
    Composer.NOTE_C_OCTAVE + 12: 'C++'
}


def get_note_name(current_note):
    if current_note and current_note in NOTE_NAME:
        return NOTE_NAME[current_note]
    else:
        return ''


def main():
    pygame.init()
    pygame.display.init()
    screen = pygame.display.set_mode((300, 150))
    screen.fill((0, 0, 0))
    pygame.display.update()
    pygame.display.set_caption('MIDI Test')
    composer = Composer()
    font = pygame.font.SysFont('Arial', 50)

    running = True
    line = []
    while running:
        event = pygame.event.wait()
        if event.type == pygame.QUIT:
            running = False
            break

        if event.type == pygame.KEYDOWN or event.type == pygame.KEYUP:
            if event.key == pygame.K_ESCAPE:
                running = False
                break
            elif event.key == pygame.K_BACKSPACE and event.type == pygame.KEYDOWN:
                line = line[:-1]
            elif event.key == pygame.K_RETURN and event.type == pygame.KEYDOWN:
                print(' '.join(line))
                line = []
            else:
                composer.process_input(event)
                new_note = get_note_name(composer.current_note)
                screen.fill((0, 0, 0))
                screen.blit(font.render(
                    new_note, True, (255, 255, 255)), (0, 0))
                pygame.display.update()
                if new_note != '' and event.type == pygame.KEYDOWN:
                    line.append(new_note)

    composer.close()
    pygame.quit()
    input('Press any key to continue...')


if __name__ == '__main__':
    main()
