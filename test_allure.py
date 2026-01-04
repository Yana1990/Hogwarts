import allure
import pytest


@allure.step("测试步骤1:打开页面")
def simple_step1(step_param1, step_param2=None):
    '''定义一个测试步骤'''
    print(f"步骤1：打开页面，参数1: {step_param1}, 参数2：{step_param2}")


@allure.step("测试步骤2:完成搜索")
def simple_step2(step_param):
    '''定义一个测试步骤'''
    print(f"步骤2：完成搜索 {step_param} 功能")


@allure.title("搜索:{param1}")
@pytest.mark.parametrize('param1', ["pytest", "allure"], ids=['search pytest', 'search allure'])
def test_parameterize_with_id(param1):
    simple_step2(param1)


@allure.title("打开页面测试:{param1},{param2}")
@pytest.mark.parametrize('param1', [True, False])
@pytest.mark.parametrize('param2', ['value 1', 'value 2'])
def test_parametrize_with_two_parameters(param1, param2):
    simple_step1(param1, param2)


@allure.title("打开页面,并搜索测试:{param1},{param2},{param3}")
@pytest.mark.parametrize('param2', ['pytest', 'unittest'])
@pytest.mark.parametrize('param1,param3', [[1, 2]])
def test_parameterize_with_uneven_value_sets(param1, param2, param3):
    simple_step1(param1, param3)
    simple_step2(param2)
