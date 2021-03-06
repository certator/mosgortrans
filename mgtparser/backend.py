# This file is part of Mosgortrans schedules parser
# Author: 2014 Dmitry Shachnev <d-shachnev@yandex.ru>
# License: BSD

import abc
import json

class Backend(metaclass=abc.ABCMeta):
	'''This is an abstract type from which all other backends should
	inherit.'''

	@abc.abstractmethod
	def get_routes_by_type(route_type):
		'''Returns a list of routes of given type.

		:param route_type: type of route
		:type route_type: :class:`~mgtparser.common.RouteType`
		:rtype: list of strings
		'''

	@abc.abstractmethod
	def get_days(self, route_type, route):
		'''Returns a list of days for which a schedule is available.
		Each day is a string of seven characters '0' or '1', representing
		days of week (called 'week string').

		:param route_type: type of route
		:param route: route number
		:type route_type: :class:`~common.RouteType`
		:type route: string
		'''

	@abc.abstractmethod
	def get_directions(self, route_type, route, day):
		'''Returns a list of directions for which a schedule is available.

		:param route_type: type of route
		:param route: route number
		:param day: day of week
		:type route_type: :class:`~common.RouteType`
		:type route: string
		:type day: either week string or an integer in ``range(7)``
		:rtype: list of strings
		'''

	@abc.abstractmethod
	def get_waypoints(self, route_type, route, day, direction):
		'''Returns a list of directions for which a schedule is available.

		:param route_type: type of route
		:param route: route number
		:param day: day of week
		:param direction: direction number
		:type route_type: :class:`~common.RouteType`
		:type route: string
		:type day: either week string or an integer in ``range(7)``
		:type direction: string, 'AB' or 'BA'
		:rtype: list of strings
		'''

	@abc.abstractmethod
	def get_schedule(self, route_type, route, day, direction, waypoint):
		'''Returns a list of directions for which a schedule is available.

		:param route_type: type of route
		:param route: route number
		:param day: day of week
		:param direction: direction number
		:param waypoint: waypoint number (if None, get schedule for all waypoints)
		:type route_type: :class:`~common.RouteType`
		:type route: string
		:type day: either week string or an integer in ``range(7)``
		:type direction: string, 'AB' or 'BA'
		:type waypoint: integer or None
		:rtype: :class:`Schedule`
		'''

class Schedule():
	'''A class representing a schedule.

	:param created: date when the schedule was created
	:type created: datetime.date structure
	:param valid: date until which the schedule is valid
	:type valid: datetime.date structure
	:param schedule: the schedule information (times is a list of 'HH:MM' strings)
	:type schedule: {waypoint: times} dictionary
	'''
	created = None
	valid = None
	schedule = None

	def get_info_string(self):
		'''Returns a string with some information about route.'''
		schedule_items = list(self.schedule.items())
		first_schedule = schedule_items[0][1]
		last_schedule = schedule_items[-1][1]
		work_hours = (int(first_schedule[-1].split(':')[0]) -
		              int(first_schedule[0].split(':')[0])) % 24
		return '%d waypoints, start %s-%s, finish %s-%s, %d routes per day, %d work hours' % (
			len(self.schedule),
			first_schedule[0], first_schedule[-1],
			last_schedule[0], last_schedule[-1],
			len(first_schedule), work_hours
		)

	def _get_dumpable_object(self):
		waypoints = {}
		wp_list = []
		for waypoint_name in self.schedule:
			waypoints[waypoint_name] = []
			wp_list += [waypoint_name]
			for time in self.schedule[waypoint_name]:
				hour, minute = time.split(':')
				if len(hour) == 1:
					hour = '0' + hour
				#if hour in waypoints[waypoint_name]:
				#	waypoints[waypoint_name][hour] += (',' + minute)
				#else:
				#	waypoints[waypoint_name][hour] = minute
				waypoints[waypoint_name] += [hour + '-' + minute]
		return {
			'created': str(self.created) if self.created else None,
			'valid': str(self.valid) if self.valid else None,
			'waypoints': waypoints,
			'waypoints_list': wp_list,
			'route': self.route,
			'day': self.day,
			'direction': self.direction,
            
		}

	def dump_json(self):
		'''Returns a JSON string representing the schedule.'''
		return json.dumps(self._get_dumpable_object(), sort_keys=True, indent=2,
			ensure_ascii=False, separators=(',', ': '))

	def save_to_file(self, filename):
		'''Saves the schedule to a JSON file.

		:param filename: file name
		:type filename: string
		'''
		with open(filename, 'w') as output:
			json.dump(self._get_dumpable_object(), output, sort_keys=True,
			indent=2, ensure_ascii=False, separators=(',', ': '))
