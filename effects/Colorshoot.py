from effects.Effect import Effect
import random


class Colorshoot(Effect):

    def __init__(self, pixel_max, strip, pixel_min=0, sleep=50, hsv=(0, 0, 0)):
        Effect.__init__(self, pixel_max=pixel_max, pixel_min=pixel_min, sleep=sleep, hsv=hsv)
        self._iterations = (pixel_max - pixel_min) * 2
        self._original_sleep = sleep

        # pixel dict
        self._pixels = []
        # time for a single fading step
        self._fading_time = 5
        # currently fading pixel
        self._current_pixel = None
        # possible states:
        #   growing: starting to light up things
        self._state = 'begin'
        self.sleep = self._fading_time

    def run(self, strip):
        if self._state == 'begin':
            # growing is starting
            strip.off()
            self._pixels = range(self.pixel_min, self.pixel_max)
            random.shuffle(self._pixels)
            self._state = 'growing'
        elif self._state == 'growing' and len(self._pixels) == 0:
            # growing is finished
            self._state = 'shrinking'
            self._pixels = range(self.pixel_min, self.pixel_max)
            random.shuffle(self._pixels)
        elif self._state == 'growing':
            # grow a pixel
            # is there already a pixel growing?
            if self._current_pixel is None:
                # no pixel growing
                self._current_pixel = self._pixels.pop()
                strip.add(position=self._current_pixel, pixel=(self.hsv[0], self.hsv[1], 0.001))
            else:
                now = strip.get(self._current_pixel)
                if now[2] > self.hsv[2]:
                    # pixel is finished
                    strip.set(position=self._current_pixel, pixel=self.hsv)
                    self._current_pixel = None
                else:
                    # pixel is still growing
                    # calculate step size
                    adding = self.hsv[2] / (self._original_sleep / float(self._fading_time))
                    strip.set(position=self._current_pixel, pixel=(self.hsv[0], self.hsv[1], now[2] + adding))
        elif self._state == 'shrinking':
            # shrink a pixel
            # is there already a pixel in move?
            if self._current_pixel is None:
                # no pixel growing
                self._current_pixel = self._pixels.pop()
                strip.add(position=self._current_pixel, pixel=(self.hsv[0], self.hsv[1], self.hsv[2]))
            else:
                now = strip.get(self._current_pixel)
                if now[2] <= 0:
                    # pixel is finished
                    strip.remove(position=self._current_pixel)
                    self._current_pixel = None
                else:
                    # pixel is still shrinking
                    # calculate step size
                    adding = self.hsv[2] / (self._original_sleep / float(self._fading_time))
                    strip.set(position=self._current_pixel, pixel=(self.hsv[0], self.hsv[1], now[2] - adding))

        return strip
