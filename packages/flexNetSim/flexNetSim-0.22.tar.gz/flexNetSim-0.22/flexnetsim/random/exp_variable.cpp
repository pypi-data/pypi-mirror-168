#include "exp_variable.hpp"

ExpVariable::ExpVariable(unsigned int seed, double parameter1) {
  if (parameter1 <= 0) {
    throw std::runtime_error("Lambda parameter must be positive.");
  }
  this->generator = std::mt19937(seed);
  this->parameter1 = parameter1;
  this->dist =
      std::uniform_real_distribution<double>(0, std::nextafter(1.0, 1.1));
}

double ExpVariable::getNextValue() {
  return (-log(1 - this->dist(this->generator)) / this->parameter1);
}
