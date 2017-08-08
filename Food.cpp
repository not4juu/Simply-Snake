#include <cstdlib>
#include <ctime>
#include <vector>

typedef std::vector<int> Point;

class Food{

private:
	int dimx;
	int dimy;
public:

    Food(int dimY, int dimX)
    {
		this->dimy = dimY;
		this->dimx = dimX;
        srand(time(NULL));
    }
    Point run()
    {      
		Point p;
       	int y = 1.0 + (rand()/(RAND_MAX + 1.0)) * dimy;
		int x = 1.0 + (rand()/(RAND_MAX + 1.0)) * dimx;
		p.push_back(y); p.push_back(x);
       	return p;
    } 
};

#include <boost/python.hpp>
#include <boost/python/suite/indexing/vector_indexing_suite.hpp>
using namespace boost::python;

BOOST_PYTHON_MODULE(food)
{
	class_<Point>("Point")
        .def(vector_indexing_suite<Point>() );

    class_<Food>("Food", init<int, int>())
        .def("run", &Food::run)
    ;

}

