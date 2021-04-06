"""Bond Calculator

This script allows the user to calculate the Yield-to-Maturity, Price, Duration, or Convexity of a bond. It is operated purely through a Command Line Interface (CLI).
"""

from pyfiglet import Figlet
import numpy as np
from scipy.optimize import newton


def _cash_flows(discount: float = 0.0, coupon: float = 0.0, face: float = 100.00, nper: int = 1) -> float:
    """Calculates the present value of a bond's cash flows.

    Parameters
    ----------
    discount : float = 0.0
        The discount rate for the cash flows (equivalently, the bond's yield)
    coupon : float = 0.0
        The coupon rate of the bond.
    face : float = 100.00
        The bond's face value, or principal amount repaid at maturity.
    nper : int = 1
        The number of payment periods.

    Returns
    -------
    float
        The present value (PV) of the bond's cash flows.
    """
    cf = np.fromfunction(lambda i: coupon*face/(1 + discount)**(i + 1), (nper,), dtype=int)
    cf[-1] += face/(1 + discount)**(cf.shape[0]) # Acount for principal repayment in last period
    return np.sum(cf) # Return PV(Cash Flows)


def _ytm() -> float:
    """Calculates a bond's Yield-to-Maturity (YTM).

    Acquires all necessary parameters through command line input.

    Returns
    -------
    float
        The YTM of the desired bond, as a decimal.
    """
    price = float(input("What is the price of this bond? $"))
    nper = int(input("What is the total number of payment periods? "))
    face = float(input("What is the face value of the bond? $"))
    coupon = float(input("What is the coupon %age per period? Enter as a number (e.g. '5' for 5%) "))/100

    return newton(lambda y: _cash_flows(y, coupon, face, nper) - price, 0.05)


def _price() -> float:
    """Calculates a bond's price.

    Acquires all necessary parameters through command line input.

    Returns
    -------
    float
        The price of the desired bond.
    """
    face = float(input("What is the face value of this bond? $"))
    apr = float(input("What is the APR of this bond? Enter as a number (e.g. '5' for 5%) "))/100
    coupon = float(input("What is the annual coupon rate of this bond? Enter as a number (e.g. '5' for 5%) "))/100
    freq = int(input("How many coupon payments per year? "))
    years = int(input("How many years to maturity? "))

    return _cash_flows(apr/freq, coupon/freq, face, freq*years)


if __name__ == '__main__':
    f = Figlet(font='slant')
    print(f.renderText('Bond Calculator'))

    exit = False
    while(not exit):
        print("---------------------------------------------")
        print("Please select one of the following functions:")
        print("    1. YTM")
        print("    2. Price")
        print("    3. Duration & Convexity")
        choice = int(input("Enter your choice as a number: "))

        if choice == 1:
            print("Yield to Maturity: {:.2f}%".format(100*_ytm()))
        elif choice == 2:
            print("Price: ${:.2f}".format(_price()))

        exit = (input("Press 'x' to exit or any key to continue: ").strip() == "x")
