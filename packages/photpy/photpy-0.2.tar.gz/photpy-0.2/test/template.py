class Fiber:

    def __init__(self,
                 length: int = 10000,
                 lam: int = 1550,
                 alpha_b: float = 1,
                 dispersion: float = 17,
                 slope: float = 0,
                 n2: float = 0,
                 eff_area: float = 80,
                 coupling: str = None
                 ) -> None:
        """
        Args:
            length: Fiber length [m]
            lam: Wavelength [nm] of fiber parameters
            alpha_b: Attenuation [dB/km]
            dispersion: Dispersion [ps/nm/km].
            slope: Slope [ps/nm^2/km]
            n2: Nonlinear index n2 [m^2/W]
            eff_area: Effective area [um^2]
        """
        self.length = length
        self.lam = lam
        self.alpha_b = alpha_b
        self.dispersion = dispersion
        self.slope = slope
        self.n2 = n2
        self.eff_area = eff_area
        self.coupling = coupling


if __name__ == '__main__':
    fiber = Fiber()  # new一个Fiber对象

    print(fiber.lam)  # Fiber对象已具有初始值
