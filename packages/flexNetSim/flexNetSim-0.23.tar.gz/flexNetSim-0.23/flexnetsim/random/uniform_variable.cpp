#include "uniform_variable.hpp"

UniformVariable::UniformVariable(unsigned int seed, double parameter1) {
  if (parameter1 < 0) {
    throw std::runtime_error("Parameter 1  must be positive.");
  }
  this->generator = std::mt19937(seed);
  this->parameter1 = parameter1;
  this->dist = std::uniform_int_distribution<int>(0, this->parameter1);
}

double UniformVariable::getNextValue(void) { return dist(this->generator); }

double UniformVariable::getNextIntValue(void) { return dist(this->generator); }
