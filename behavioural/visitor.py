"""
The Visitor patterns represents an operation to be performed on elements of an object structure.
Visitor lets you define a new operation without changing the classes of the elements on which it operates.
"""

from abc import ABCMeta, abstractmethod
from functools import singledispatch

# ABC stands for Abstract Base Class (the abc module is part of the standard library of python 2)
# The ABCMeta allows to define an abstract class and to enforce its API to the concrecte classes implementing it 

class VisitableBase(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def accept(self, visitor):
        pass

class EmployeeBase(VisitableBase):

    def accept(self, visitor):
        visitor.visit(self)

class Executive(EmployeeBase):
    def get_dividends(self):
        return 1000

    def get_base_salary(self):
        return 90000

    def get_bonus(self):
        return 15000


class Engineer(EmployeeBase):
    def get_bonus(self):
        return 4000

    def get_base_salary(self):
        return 75000

class TruckDriver(EmployeeBase):
    def get_hourly_rate(self):
        return 18

    def get_hours_worked(self):
        return 1820

    def get_vehicle_expenses(self):
        return 20000

class EmployeeVisitorBase(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    @singledispatch
    def visit(self, element):
        pass

    @visit.register(Executive)
    @abstractmethod
    def visit_executive(self, executive):
        pass

    @visit.register(Engineer)
    @abstractmethod
    def visit_engineer(self, engineer):
        pass

    @visit.register(TruckDriver)
    @abstractmethod
    def visit_truck_driver(self, truck_driver):
        pass


class SalaryCalculator(EmployeeVisitorBase):
    def __init__(self):
        self.salary = 0

    def visit_executive(self, executive):
        self.salary = executive.get_dividends() + executive.get_base_salary() + executive.get_bonus()

    def visit_engineer(self, engineer):
        self.salary = engineer.get_bonus() + engineer.get_base_salary()

    def visit_truck_driver(self, truck_driver):
        self.salary = truck_driver.get_hourly_rate() * truck_driver.get_hours_worked() + truck_driver.get_vehicle_expenses()

    def calculate(self):
        return self.salary

if __name__ == "__main__":
    employees = [Engineer()] * 10 + [TruckDriver()] * 20 + [Executive] # 10 Engineers, 20 Truck Drivers, 1 Executive
    salary_calculator = SalaryCalculator()
    total_salaries = 0

    for employee in employees:
#        salary_calculator.visit(
        employee.accept(salary_calculator)
        total_salaries = total_salaries + salary_calculator.calculate()
