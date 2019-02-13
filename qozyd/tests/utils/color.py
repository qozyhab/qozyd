from qozyd.utils.color import RGB, HSV, HSL, Color
from unittest import TestCase


class ColorTest(TestCase):
    def test_baseclasss(self):
        color = Color()

        with self.assertRaises(NotImplementedError):
            color.from_rgb(0, 0, 0)

        with self.assertRaises(NotImplementedError):
            color.rgb()

    def test_from_rgb(self):
        color = RGB.from_rgb(255, 255, 0)
        self.assertEqual(color.r, 255)
        self.assertEqual(color.g, 255)
        self.assertEqual(color.b, 0)

        self.assertEqual(color.__json__(), (255, 255, 0))

        color = HSV.from_rgb(255, 255, 0)
        self.assertEqual(color.h, 60)
        self.assertEqual(color.s, 100)
        self.assertEqual(color.v, 100)

        color = HSL.from_rgb(255, 255, 0)
        self.assertEqual(color.h, 60)
        self.assertEqual(color.s, 100)
        self.assertEqual(color.l, 50)

    def test_rgb(self):
        color = RGB(255, 255, 0)
        self.assertEqual(color.rgb(), (255, 255, 0))

        color = HSV(60, 100, 100)
        self.assertEqual(color.rgb(), (255, 255, 0))

        color = HSL(60, 100, 50)
        self.assertEqual(color.rgb(), (255, 255, 0))

    def test_convert(self):
        rgb = RGB(255, 255, 0)

        hsv = rgb.convert(HSV)
        self.assertEqual(hsv.h, 60)
        self.assertEqual(hsv.s, 100)
        self.assertEqual(hsv.v, 100)

        hsl = rgb.convert(HSL)
        self.assertEqual(hsl.h, 60)
        self.assertEqual(hsl.s, 100)
        self.assertEqual(hsl.l, 50)

        hsl = hsv.convert(HSL)
        self.assertEqual(hsl.h, 60)
        self.assertEqual(hsl.s, 100)
        self.assertEqual(hsl.l, 50)

        hsv = hsl.convert(HSV)
        self.assertEqual(hsv.h, 60)
        self.assertEqual(hsv.s, 100)
        self.assertEqual(hsv.v, 100)

        rgb = hsv.convert(RGB)
        self.assertEqual(rgb.r, 255)
        self.assertEqual(rgb.g, 255)
        self.assertEqual(rgb.b, 0)

        rgb = hsl.convert(RGB)
        self.assertEqual(rgb.r, 255)
        self.assertEqual(rgb.g, 255)
        self.assertEqual(rgb.b, 0)
