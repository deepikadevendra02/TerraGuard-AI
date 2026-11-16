import unittest
from risk_engine import assess_risk

class RiskEngineTests(unittest.TestCase):
    def test_high_rainfall_and_saturation_increase_score(self):
        low=assess_risk({"rainfall_mm_24h":10,"slope_deg":10,"soil_saturation_pct":20,"landslide_history":0})
        high=assess_risk({"rainfall_mm_24h":200,"slope_deg":40,"soil_saturation_pct":90,"landslide_history":1})
        self.assertGreater(high["risk_score"],low["risk_score"])
    def test_invalid_slope_rejected(self):
        with self.assertRaises(ValueError):
            assess_risk({"rainfall_mm_24h":10,"slope_deg":120,"soil_saturation_pct":20,"landslide_history":0})
    def test_output_has_disclaimer(self):
        r=assess_risk({"rainfall_mm_24h":50,"slope_deg":20,"soil_saturation_pct":40,"landslide_history":0})
        self.assertIn("not a validated forecast",r["disclaimer"].lower())
if __name__=="__main__": unittest.main()
