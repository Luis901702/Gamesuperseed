# sounds.py
import pygame
import random

class SoundManager:
    def __init__(self):
        # Inicializar el mixer antes de cualquier operación de sonido
        try:
            pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=512)
            print("pygame.mixer inicializado correctamente")
        except pygame.error as e:
            print(f"Error al inicializar pygame.mixer: {e}")

        self.sounds = {}

        # Cargar efectos de sonido
        try:
            self.sounds["hero_attack1"] = pygame.mixer.Sound("assets/sounds/hero_attack1.wav")
            self.sounds["hero_attack2"] = pygame.mixer.Sound("assets/sounds/hero_attack2.wav")
            self.sounds["enemy_defeated"] = pygame.mixer.Sound("assets/sounds/enemy_defeated.wav")
            self.sounds["enemy_attack"] = pygame.mixer.Sound("assets/sounds/enemy_attack.wav")
            self.sounds["level_up"] = pygame.mixer.Sound("assets/sounds/level_up.wav")
            print("Efectos de sonido cargados correctamente")
        except pygame.error as e:
            print(f"Error al cargar sonidos: {e}")
            for key in ["hero_attack1", "hero_attack2", "enemy_defeated", "enemy_attack", "level_up"]:
                if key not in self.sounds:
                    self.sounds[key] = pygame.mixer.Sound(pygame.mixer.Sound(buffer=b'\x00' * 1000))

        # Configurar volumen de efectos de sonido
        for sound in self.sounds.values():
            sound.set_volume(0.5)  # Volumen de efectos al 50%

        # Cargar y configurar música de fondo
        try:
            pygame.mixer.music.load("assets/sounds/background_music.mp3")
            pygame.mixer.music.set_volume(0.3)  # Subimos a 0.3 para pruebas, ajusta si es necesario
            print("Música de fondo 'background_music.mp3' cargada correctamente")
        except pygame.error as e:
            print(f"Error al cargar la música de fondo: {e}")

    def play(self, sound_name):
        if sound_name in self.sounds:
            self.sounds[sound_name].play()
        else:
            print(f"Sonido '{sound_name}' no encontrado")

    def play_random_hero_attack(self):
        hero_attacks = ["hero_attack1", "hero_attack2"]
        chosen_sound = random.choice(hero_attacks)
        self.play(chosen_sound)

    def stop(self, sound_name):
        if sound_name in self.sounds:
            self.sounds[sound_name].stop()

    def set_volume(self, sound_name, volume):
        if sound_name in self.sounds:
            self.sounds[sound_name].set_volume(volume)

    def play_background_music(self):
        """Inicia la música de fondo en bucle."""
        try:
            pygame.mixer.music.play(loops=-1)  # -1 para bucle infinito
            print("Reproduciendo música de fondo en bucle")
        except pygame.error as e:
            print(f"Error al reproducir la música de fondo: {e}")

    def stop_background_music(self):
        """Detiene la música de fondo."""
        pygame.mixer.music.stop()
        print("Música de fondo detenida")

    def set_background_volume(self, volume):
        """Ajusta el volumen de la música de fondo."""
        pygame.mixer.music.set_volume(volume)
        print(f"Volumen de música de fondo ajustado a {volume}")