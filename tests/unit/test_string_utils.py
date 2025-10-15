import pytest
import allure
from unittest.mock import patch

from framework.utils import string_utils


@allure.feature("Framework")
@allure.story("String Utils")
@pytest.mark.unit
class TestStringUtils:
    
    @allure.title("Test mask secret returns masked string")
    def test_mask_secret(self):
        result = string_utils.mask_secret()
        
        assert result == "***"
        assert isinstance(result, str)
    
    @allure.title("Test mask secret consistency")
    def test_mask_secret_consistency(self):
        # Call multiple times to ensure consistent behavior
        result1 = string_utils.mask_secret()
        result2 = string_utils.mask_secret()
        
        assert result1 == result2
        assert result1 == "***"