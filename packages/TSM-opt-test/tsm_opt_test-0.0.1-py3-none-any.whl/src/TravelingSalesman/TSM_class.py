#  Copyright (c) 2021. | by: Tommer Rissin | github: github.com/Tommer-R

import random
from datetime import timedelta
from math import dist
from time import time

import matplotlib.pyplot as plt
import numpy as np


class TSM:
    def __init__(self, locations: int = 10, circle: bool = False, render=False) -> None:
        """
        generates n 2D locations on matrix of 1000*1000 in circle shape or random scatter to
        test optimization algorithms.
        :param locations: the number of locations to generate
        :param circle: generate locations in circle shape. this allows calculating the optimal distance without solving
        """
        self.__circle: bool = circle  # if locations should be arranged in a circle
        self.do_render = render  # show live plot or not
        # dict with location ID as key and location in tuple {1:(10,42)}
        self.score_history = []  # used for rendering
        self.locations: dict = self.__gen_locations(locations)  # generate the locations dict
        self.__initial_route: list = list(self.locations.keys())  # optimal state in circle form, first state in general
        self.adjacency_lists = self.__calc_adjacency_matrix()  # create list
        self.__start_time = time()

        if render:
            # define and adjust figure
            self.fig = plt.figure(figsize=(16, 8), facecolor='#DEDEDE')
            self.ax = plt.subplot(1, 2, 1)
            self.ax1 = plt.subplot(1, 2, 2)
            self.ax.set_facecolor('#DEDEDE')
            self.ax1.set_facecolor('#DEDEDE')
            self.__rendered = True  # created plot variables
        else:
            self.__rendered = False

        self.__initial_distance: float = self.__distance_calculation(self.__initial_route)  # initial route distance
        self.score_history = []  # used for rendering

        if locations > 800:  # when above 800 the hard distance calculation is faster
            self.route_distance = self.__distance_calculation
        else:  # under 800 calculation using matrix calculation is faster
            self.route_distance = self.__distance_matrix_calculation

    # generate a list of random cities
    def __gen_locations(self, locations: int) -> dict:  # generate dict of locations
        result: dict = {}
        if self.__circle:  # arrange locations in a circle
            center = [locations, locations]
            radius = 0.8 * locations
            count = 0
            for angle in np.linspace(0, 2 * np.pi, locations, endpoint=False):
                result[count] = (center[0] + np.sin(angle) * radius, center[1] + np.cos(angle) * radius)
                count += 1

            return result

        elif not self.__circle:  # arrange locations randomly
            for i in range(locations):  # create n locations
                result[i] = (random.randint(1, 1000), random.randint(1, 1000))
            return result

    # add one new location with input coordinates
    def add_location(self, x: int, y: int, name: any = None) -> None:
        for i in {x, y}:
            if type(i) not in {int, float}:
                raise ValueError(f'x and y must be numbers')

        if name is not None:
            new_key = name
        else:
            new_key = 1
            while True:
                if new_key not in self.locations.keys():
                    break
                else:
                    new_key += 1

        self.locations[new_key] = (x, y)
        self.__initial_route.append(new_key)
        self.__initial_distance = self.__distance_calculation(self.__initial_route)  # distance of op_route
        self.reset()

    # calculate the sum distance of a route
    def __distance_calculation(self, route: list = None, ) -> float:
        """
        calculates the total distance of the input state.
        :param route: list of ID keys of the locations.
        :return: float of sum state distance.
        """
        res = 0
        for i in range(len(route) - 1):  # iterate locations and sum distances
            a = self.locations[route[i]]  # first location
            b = self.locations[route[i + 1]]  # second location
            distance = dist(a, b)  # distance between the 2 locations
            res += distance  # add distance to sum
        self.score_history.append(res)

        if self.do_render and len(self.score_history) % self.do_render == 0:
            self.render(route)
        return res

    def __distance_matrix_calculation(self, route: list = None):
        """
        calculates the total distance of the input state.
        :param route: list of ID keys of the locations.
        :return: float of sum state distance.
        """
        res = 0
        for i in range(len(route) - 1):
            res += self.adjacency_lists[route[i]][route[i + 1]]
        self.score_history.append(res)
        if self.do_render and len(self.score_history) % self.do_render == 0:
            self.render(route)
        return res

    def __calc_adjacency_matrix(self):
        adjacency_lists = []

        for coor in list(self.locations.values()):
            temp = []
            for coor2 in list(self.locations.values()):
                temp.append(dist(coor, coor2))
            adjacency_lists.append(temp)

        return adjacency_lists

    # show a plot of the locations and a route if there is one
    def plot(self, route: list = None, labels: bool = False) -> None:
        """
        plots the locations in a scatter plot and route if provided or the first route
        :param route: list of location ID's in as the route
        :param labels: show ID's on top of scatter plot.
        """
        if route is None:  # if state is empty use start_route
            x = [self.locations[key][0] for key in self.__initial_route]
            y = [self.locations[key][1] for key in self.__initial_route]
            plt.title(f'Distance: {round(self.route_distance(route=self.__initial_route), 1)}')
        else:  # use input state
            x = [self.locations[key][0] for key in route]
            y = [self.locations[key][1] for key in route]
            plt.title(f'Distance: {round(self.route_distance(route=route), 1)}')
        plt.plot(x, y, zorder=1)  # plot the state
        plt.scatter(x, y, s=50, c='red', zorder=2)  # scatter the locations
        for i in self.locations.keys():  # create labels
            x = self.locations[i][0]
            y = self.locations[i][1]
            label = str(i)
            if labels:  # add labels to plot
                plt.annotate(label, (x, y), xytext=(0, 10), textcoords="offset points", ha='center')
        plt.show()

    def random_route(self, seed: any = None) -> list:
        """
        :param seed: the seed for random functions
        :return: a list representing a randomized route
        """
        result: list = self.__initial_route.copy()  # random state
        if seed is not None:
            random.seed(seed)
        random.shuffle(result)  # shuffle the random state

        return result

    # function to update the data
    def render(self, route: list):

        if not self.__rendered:
            # define and adjust figure
            self.fig = plt.figure(figsize=(16, 8), facecolor='#DEDEDE')
            self.ax = plt.subplot(1, 2, 1)
            self.ax1 = plt.subplot(1, 2, 2)
            self.ax.set_facecolor('#DEDEDE')
            self.ax1.set_facecolor('#DEDEDE')
            self.__rendered = True

        # clear axis
        plt.ioff()
        self.ax.cla()
        self.ax1.cla()

        # plot locations
        x, y = [], []
        for i in route:
            x.append(self.locations[i][0])
            y.append(self.locations[i][1])

        self.ax.plot(x, y, 'co')

        # Set a scale for the arrow heads (there should be a reasonable default for this, WTF?)
        a_scale = float(max(x)) / float(100)

        # Draw the route for the TSP problem
        for i in range(0, len(x) - 1):
            self.ax.arrow(x[i], y[i], (x[i + 1] - x[i]), (y[i + 1] - y[i]), head_width=a_scale,
                          color='g', length_includes_head=True)

        # Set axis too slightly larger than the set of x and y
        self.ax.set_xlim(0, max(x) * 1.1)
        self.ax.set_ylim(0, max(y) * 1.1)
        self.ax.set_aspect('equal', 'datalim')  # make use ax is a square
        self.ax.set_ylabel('y coordinates')
        self.ax.set_xlabel('x coordinates')
        self.ax.set_title('route')

        # plot score progress
        self.ax1.plot(self.score_history)
        self.ax1.scatter(len(self.score_history) - 1, self.score_history[-1])
        self.ax1.text(len(self.score_history) - 1, self.score_history[-1] + 2, str(int(self.score_history[-1])))
        self.ax1.set_ylabel('distance')
        self.ax1.set_xlabel('function calls')
        self.ax1.set_title('distance improvement')

        run_time = timedelta(seconds=round(time() - self.__start_time))
        self.fig.suptitle(f'Route distance: {str(round(self.score_history[-1], 2))}   |   '
                          f'best distance: {str(round(min(self.score_history), 2))}   |   '
                          f'distance function calls: {len(self.score_history)}   |   '
                          f'run time: {run_time}', fontsize=16)
        plt.show(block=False)
        plt.pause(0.0000001)

        # plt.savefig(f'C:\\Users\\Tommer\\PycharmProjects\\sa_solver\\TravelingSalesman\\figs/fig_'
        #            f'{len(self.score_history)}.png')

    def reset(self):
        self.__initial_route: list = list(self.locations.keys())  # optimal state in circle form, first state in general
        self.score_history = []
        self.adjacency_lists = self.__calc_adjacency_matrix()
        if len(self.locations) > 800:  # when above 800 the hard distance calculation is faster
            self.route_distance = self.__distance_calculation
        else:  # under 800 calculation using matrix calculation is faster
            self.route_distance = self.__distance_matrix_calculation

    @property
    def adjacency_matrix(self):
        return np.array(self.adjacency_lists)

    @property
    def circle(self):
        return self.__circle

    @property
    def initial_route(self):
        return self.__initial_route
