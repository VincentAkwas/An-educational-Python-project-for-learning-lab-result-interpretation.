
Lab Result Interpreter - Core Module
A comprehensive Python tool for interpreting medical laboratory test results.
Educational tool only - not for clinical decision making.
"""

from dataclasses import dataclass
from typing import Dict, List, Optional
from enum import Enum


class ResultStatus(Enum):
    """Status of a lab result compared to reference range."""
    NORMAL = "NORMAL"
    LOW = "LOW"
    HIGH = "HIGH"
    CRITICAL_LOW = "CRITICAL_LOW"
    CRITICAL_HIGH = "CRITICAL_HIGH"


@dataclass
class ReferenceRange:
    """Reference range for a lab test value."""
    min_value: float
    max_value: float
    critical_low: Optional[float] = None
    critical_high: Optional[float] = None
    unit: str = ""
    
    def get_status(self, value: float) -> ResultStatus:
        """Determine the status of a value against reference range."""
        if self.critical_low is not None and value < self.critical_low:
            return ResultStatus.CRITICAL_LOW
        if self.critical_high is not None and value > self.critical_high:
            return ResultStatus.CRITICAL_HIGH
        if value < self.min_value:
            return ResultStatus.LOW
        if value > self.max_value:
            return ResultStatus.HIGH
        return ResultStatus.NORMAL


@dataclass
class TestResult:
    """Individual test result with interpretation."""
    test_name: str
    value: float
    unit: str
    reference_range: ReferenceRange
    status: ResultStatus
    interpretation: str
    clinical_significance: str


class LabTest:
    """Base class for all lab tests."""
    
    def __init__(self):
        self.results: Dict[str, TestResult] = {}
        self.test_name = "Base Lab Test"
        self.reference_ranges: Dict[str, ReferenceRange] = {}
        self.interpretations: Dict[str, Dict[str, str]] = {}
    
    def interpret_result(self, test_code: str, value: float) -> TestResult:
        """Interpret a single test result."""
        if test_code not in self.reference_ranges:
            raise ValueError(f"Unknown test code: {test_code}")
        
        ref_range = self.reference_ranges[test_code]
        status = ref_range.get_status(value)
        interpretation = self.interpretations.get(test_code, {}).get(status.value, "See reference ranges.")
        
        result = TestResult(
            test_name=test_code,
            value=value,
            unit=ref_range.unit,
            reference_range=ref_range,
            status=status,
            interpretation=interpretation,
            clinical_significance=f"Normal range: {ref_range.min_value}-{ref_range.max_value} {ref_range.unit}"
        )
        
        self.results[test_code] = result
        return result


class CompleteBloodCount(LabTest):
    """Complete Blood Count (CBC) - measures different blood cell types."""
    
    def __init__(self):
        super().__init__()
        self.test_name = "Complete Blood Count (CBC)"
        self.reference_ranges = {
            'WBC': ReferenceRange(4.5, 11.0, critical_low=2.0, critical_high=20.0, unit="10^3/µL"),
            'RBC': ReferenceRange(4.5, 5.9, critical_low=2.0, critical_high=7.0, unit="10^6/µL"),
            'Hemoglobin': ReferenceRange(13.5, 17.5, critical_low=7.0, critical_high=20.0, unit="g/dL"),
            'Hematocrit': ReferenceRange(41, 53, critical_low=20, critical_high=70, unit="%"),
            'MCV': ReferenceRange(80, 100, unit="fL"),
            'Platelets': ReferenceRange(150, 400, critical_low=50, critical_high=800, unit="10^3/µL"),
        }
        self.interpretations = {
            'WBC': {
                'HIGH': "Elevated white blood cells may indicate infection, inflammation, or leukemia.",
                'LOW': "Low white blood cells may indicate bone marrow disorder, autoimmune disease, or medication side effects.",
            },
            'RBC': {
                'HIGH': "Elevated RBC may indicate dehydration, polycythemia, or chronic hypoxia.",
                'LOW': "Low RBC may indicate anemia, blood loss, or bone marrow failure.",
            },
            'Hemoglobin': {
                'HIGH': "Elevated hemoglobin may indicate dehydration or polycythemia.",
                'LOW': "Low hemoglobin indicates anemia - check MCV to determine type.",
            },
            'Hematocrit': {
                'HIGH': "Elevated hematocrit may indicate dehydration or polycythemia.",
                'LOW': "Low hematocrit indicates anemia or blood loss.",
            },
            'MCV': {
                'HIGH': "High MCV (macrocytic anemia) - may indicate B12/folate deficiency or reticulocytosis.",
                'LOW': "Low MCV (microcytic anemia) - may indicate iron deficiency or thalassemia.",
            },
            'Platelets': {
                'HIGH': "Elevated platelets may indicate inflammation, malignancy, or essential thrombocythemia.",
                'LOW': "Low platelets (thrombocytopenia) increases bleeding risk and requires investigation.",
            },
        }


class BasicMetabolicPanel(LabTest):
    """Basic Metabolic Panel (BMP) - measures electrolytes, kidney and liver function."""
    
    def __init__(self):
        super().__init__()
        self.test_name = "Basic Metabolic Panel (BMP)"
        self.reference_ranges = {
            'Sodium': ReferenceRange(136, 145, critical_low=120, critical_high=160, unit="mEq/L"),
            'Potassium': ReferenceRange(3.5, 5.0, critical_low=2.8, critical_high=6.0, unit="mEq/L"),
            'Chloride': ReferenceRange(98, 107, unit="mEq/L"),
            'CO2': ReferenceRange(23, 29, unit="mEq/L"),
            'BUN': ReferenceRange(7, 20, critical_high=100, unit="mg/dL"),
            'Creatinine': ReferenceRange(0.7, 1.3, critical_high=4.0, unit="mg/dL"),
            'Glucose': ReferenceRange(70, 100, critical_low=40, critical_high=400, unit="mg/dL"),
            'Calcium': ReferenceRange(8.5, 10.2, critical_low=6.5, critical_high=13.0, unit="mg/dL"),
        }
        self.interpretations = {
            'Sodium': {
                'HIGH': "Hypernatremia - may indicate dehydration or diabetes insipidus.",
                'LOW': "Hyponatremia - may indicate SIADH, heart/kidney/liver disease, or excess water intake.",
            },
            'Potassium': {
                'HIGH': "Hyperkalemia - dangerous for heart; may indicate kidney failure or excessive supplementation.",
                'LOW': "Hypokalemia - may cause muscle weakness; check diuretic use and diarrhea.",
            },
            'Glucose': {
                'HIGH': "Hyperglycemia - may indicate diabetes, stress, or prednisone use.",
                'LOW': "Hypoglycemia - requires immediate evaluation; risk of seizure/coma.",
            },
            'BUN': {
                'HIGH': "Elevated BUN may indicate kidney disease, dehydration, or high protein diet.",
                'LOW': "Low BUN may indicate liver disease, malnutrition, or overhydration.",
            },
            'Creatinine': {
                'HIGH': "Elevated creatinine indicates reduced kidney function - calculate GFR.",
                'LOW': "Low creatinine may indicate low muscle mass or liver disease.",
            },
        }


class LipidPanel(LabTest):
    """Lipid Panel - measures cholesterol and triglycerides for cardiovascular risk."""
    
    def __init__(self):
        super().__init__()
        self.test_name = "Lipid Panel"
        self.reference_ranges = {
            'Total_Cholesterol': ReferenceRange(0, 200, unit="mg/dL"),
            'LDL': ReferenceRange(0, 100, unit="mg/dL"),
            'HDL': ReferenceRange(40, 300, unit="mg/dL"),
            'Triglycerides': ReferenceRange(0, 150, unit="mg/dL"),
        }
        self.interpretations = {
            'Total_Cholesterol': {
                'HIGH': "High total cholesterol increases cardiovascular disease risk.",
                'NORMAL': "Optimal cholesterol level for cardiovascular health.",
            },
            'LDL': {
                'HIGH': "High LDL ('bad' cholesterol) increases heart attack and stroke risk.",
                'NORMAL': "LDL at optimal level reduces cardiovascular disease risk.",
            },
            'HDL': {
                'LOW': "Low HDL ('good' cholesterol) increases cardiovascular disease risk.",
                'HIGH': "High HDL protects against cardiovascular disease.",
            },
            'Triglycerides': {
                'HIGH': "High triglycerides increase cardiovascular disease risk and pancreatitis risk.",
                'NORMAL': "Normal triglyceride level reduces cardiovascular risk.",
            },
        }


class LabInterpreter:
    """Main interpreter - manages all lab tests."""
    
    def __init__(self):
        self.tests = {
            'CBC': CompleteBloodCount(),
            'BMP': BasicMetabolicPanel(),
            'LP': LipidPanel(),
        }
    
    def interpret(self, test_type: str, test_code: str, value: float) -> TestResult:
        """Interpret a single test result."""
        if test_type not in self.tests:
            raise ValueError(f"Unknown test type: {test_type}")
        
        return self.tests[test_type].interpret_result(test_code, value)
    
    def get_available_tests(self) -> Dict[str, List[str]]:
        """Get all available test codes."""
        return {
            test_type: list(test.reference_ranges.keys())
            for test_type, test in self.tests.items()
        }
