# Sabacc -- an interesting card game similar to Blackjack.
# Copyright (C) 2007-2008 Joel Cross.
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.

"""
txtInterface.py (rewrite of back.Interfaces.txtInterface from 0.6 'Ackbar')
This module contains a text-based interface and application.
"""
import sys, nullInterface
from back.settings import CARDNAMES, CARDVALUE#!

##'Shift' and self.current_text are still a bit messed up. Sort out later!
## Plus, case-insensitive names for win32.
## And (single player) play needs more work
## Should show number of cards belonging to others
## Should XML agents be saved afterwards?
class gameInterface (nullInterface.gameInterface):
	"""
	This is a simple text-based game interface.
	"""
	display = []
	def update_display(self):
		'''Writes useful information and the contents of the
		display variable to the screen.'''
		from sabacc.back.Game import players_in_game, hand_pot, sabacc_pot
		
		print "===Sabacc===\n"
		print "Players in Game: %(players)s\tHand pot: %(hand)s\tSabacc pot: %(sabacc)s\n" \
			%{'players': players_in_game, 'hand': hand_pot, 'sabacc': sabacc_pot}
		
		# Print out text
		for text in gameInterface.display:
			print text
		print
		
	def write(self, text):
		'''Writes the given text to the display.'''
		from datetime import datetime
		now = datetime.today().strftime("(%H:%M:%S) ")
		gameInterface.display.insert(0, now + text)
		
		if len(gameInterface.display) > 6:
			gameInterface.display = gameInterface.display[:6]
		

class playerInterface (nullInterface.playerInterface):
	"""
	This is a simple text-based player interface.
	"""
	def __init__(self, name=None):#!name should not be optional!
		self.name = name
		self.cards = None
		self.current_text = None
	
	def show_cards(self, cards, name=None, show_all=False):
		'''Shows the given cards to the user.'''
		#! May be passed bad arguments
		if type(name) == bool:
			show_all = name
			name = None
		
		# user friendly cards array
		user_cards = []
		score = 0
		
		for x in cards:
			user_cards.append(CARDNAMES[x])
			score += CARDVALUE[x]
		
		# Method could be used for current player or another
		if name==None:
			name_has = "You have"
		else:
			name_has = name + " has"
		
		if len(user_cards) == 0:
			what_cards = " no cards"
		else:
			what_cards = " cards " + str(user_cards)
		
		self.cards = name_has + what_cards + ". Total score = " + str(score) + "."
	
	def show_num_cards(self, numcards, name):
		'''Shows the given number of cards, along with the given name.'''
		print name + " has " + str(numcards) + " cards."
		
	def get_move(self, cards):
		'''Prompts the user for the next move to take.'''
		
		self._new_turn()
		
		query = "Which move do you want to make?\n"
		options1 = """
Please choose from the following:
	stick:	Stick (default)
	draw:	Draw another card"""
		calloptions = """
	call:	Call the hand"""
		options2 = """
	exit:	Pull out of the game
	help:	Show this message
"""
		prompt = "> "
	
		validoptions = 'stick draw exit help ?'.split()
		validoptions.append('')
		
		from sabacc.back.Game import callable
		
		# Is game callable? If so, add that as an option.
		if callable:
			options1 += calloptions
		validoptions.append('call')
		
		options = options1+options2
		fullquery = query+options+prompt
		
		answer = None
		while answer == None:
			self.current_text = fullquery
			try:
				# Get answer from keyboard
				answer=raw_input(fullquery)
			except EOFError:
				print
			except KeyboardInterrupt:
				print
				answer = 'exit'
			
			# Keep asking until a valid answer is given
			if answer not in validoptions:
				fullquery = errorq+prompt
				answer=None
			elif answer in 'help ?'.split():
				fullquery = options+prompt
				answer = None
			else:
				self.current_text = None
				if answer in ['stick', '']:
					print 'Doing nothing...'
					code = 1
				elif answer == 'draw':
					print 'Drawing another card...'
					code = 0
				elif answer == 'call':
					print 'Calling the hand...'
					code = 2
				else: # exit
					print 'Leaving the game...'
					code = -1
				
		return code

	def get_bet(self, cards, mustMatch):
		'''Prompts the user for the next bet to make.'''
		
		self._new_turn()
		
		query = "Please enter the amount that you wish to bet\n"
		options1 = """
You must bet at least """ + str(mustMatch) + """ credits. This is the default option.
Betting this many credits will end the betting round."""
		calloptions = """
Entering 'call' will call the hand."""
		options2 = """
Entering 'exit' will cause you to pull out of the game.
Entering 'help' will display this message.
"""
		prompt = "> "
	
		validoptions = 'exit help ?'.split()
		
		from sabacc.back.Game import callable
		
		# Is game callable? If so, add that as an option.
		if callable:
			options1 += calloptions
		validoptions.append('call')
		
		options = options1+options2
		fullquery = query+options+prompt
		
		answer = None
		while answer == None:
			self.current_text = fullquery
			try:
				# Get answer from keyboard
				answer=raw_input(fullquery)
			except EOFError:
				print
			except KeyboardInterrupt:
				print
				answer = 'exit'
			
			# Keep asking until a valid answer is given
			if answer not in validoptions:
				# Answer may be numeric - let's try
				try:
					answer = int(answer)
				except ValueError:
					if answer == '':
						answer = mustMatch
					else:
						fullquery = errorq+prompt
						answer=None
				except TypeError:
					fullquery = errorq+prompt
					answer=None
				
				if type(answer) == int:
					if answer < mustMatch:
						fullquery="You must bet at least " + str(mustMatch) + " credits.\n" + prompt
						answer=None
					else:
						print "Betting %s credits..." %answer
						code = answer
			
			elif answer in 'help ?'.split():
				fullquery = options+prompt
				answer = None
			else:
				self.current_text = None
				if answer == 'call':
					print 'Calling the hand...'
					code = -2
				else: # exit
					print 'Leaving the game...'
					code = -1
				
		return code
		
	def game_status(self, won, cards, credits=None):
		'''Report the status of the game and any winnings to the user.'''
		self._new_turn(show_cards=False, pause=False)
		
		if won: # if player won
			message="Congratulations. You have won!\n"
		else:
			message="Sorry. You didn't win this time.\n"
		
		# Tell user whether won or not, then display cards
		self.show_cards(cards)
		
		if credits != None:
			credmod = "You now have " + str(credits) + " credits.\n"
		else:
			credmod = ""
			
		# Make sure the user has seen his status
		continue_text = "Press enter to continue...\n"
		final_msg = message + self.cards + "\n" + credmod + continue_text
		self.current_text = final_msg
		raw_input(final_msg)
		self.current_text = None
		
	def shift(self, cards):
		'''Shows the player his cards after a Sabacc shift'''
		self.show_cards(cards)
		self._new_turn(pause=False)
		
	def _new_turn(self, show_cards=True, pause=True):
		'''Prepare the screen for the next turn,
		or show correct details after a Shift.'''
		clear_screen()
		from sabacc.back import Game
		Game.interface.update_display()
		
		if humans_in_game >= 2:
			if pause:
				continue_text = self.name + "'s turn. Press enter to continue...\n"
				self.current_text = continue_text
				raw_input(continue_text)
				self.current_text = None
			else:
				print "Message for " + self.name + ":"
		
		# Show cards and number of credits
		if show_cards:
			agent = self._get_agent()
			print self.cards
			print 'You have %s credits.' %agent.credits
		
		if self.current_text:
			# Not 'print', as this leaves a gap afterwards
			sys.stdout.write(self.current_text)
	
	def _get_agent(self):
		'''If the agent is loaded in the game, returns it.'''
		
		from sabacc.back import Game
		
		if self.name not in Game.names:
			return
		
		index = Game.names.index(self.name)
		return Game.loaded[index][0]
	
	#! Old function names
	showCards = show_cards
	showNumCards = show_num_cards
	getMove = get_move
	getBet = get_bet
	gameStatus = game_status

'''
Begin Application
'''
humans_in_game = 0
errorq="Sorry. That is not a valid option. Please try again.\n"

def start_app():
	'''Starts the application and prompts for next move'''
	clear_screen()
	header = "===Sabacc Text Interface===\n"
	query = "Welcome to Sabacc. What do you want to do?\n"
	options = """
Please choose from the following:
	play:	Play the game
	agent:	Create or modify a computer agent
	help:	Display this screen
	quit:	Quit Sabacc
"""
	prompt = "> "
	print header
	
	validoptions = 'play agent help quit ?'.split()
	
	fullquery = query+options+prompt
	
	while True:
		answer = None
		try:
			answer=raw_input(fullquery)
		except EOFError:
			print
			answer = "quit"
		
		# Keep asking until a valid answer is given
		if answer not in validoptions:
			if answer == "":
				fullquery = prompt
			else:
				fullquery = errorq+prompt
		elif answer in 'help ?'.split():
			fullquery = options+prompt
		else:
			if answer == "play":
				play_menu()
			elif answer == "agent":
				agent_menu()
			else: # quit
				break
			fullquery = query+options+prompt

def clear_screen():
	'''Runs the system's 'cls' or 'clear' command'''
	import os, sys
	
	if sys.platform == 'win32':
		clearcommand = 'cls'
	else:
		clearcommand = 'clear'
		
	os.system(clearcommand)

def play_menu():
	'''Contains menus for adding/removing  players and starting the game.'''
	query = "Welcome to the Sabacc Game Interface\n"
	optionslist = ["\nPlease choose from the following:", """
	add_human:	Add a human player to the game
	add_computer:	Add a computer player to the game""", """
	remove:		Remove a player from the game""", """
	start:		Start the game""", """
	show:		Show status of game
	help:		Display this screen
	quit:		Return to the main menu
"""]
	# Create correct options list (instructions + add + help/quit)
	validoptions = 'add_human add_computer show help quit ?'.split()
	options = optionslist[0] + optionslist[1] + optionslist[4]
	
	prompt = "> "
	fullquery = query+options+prompt
	
	while True:
		answer = None
		try:
			answer=raw_input(fullquery)
		except EOFError:
			print
			answer = "quit"
		
		# Keep asking until a valid answer is given
		if answer not in validoptions:
			if answer == "":
				fullquery = prompt
			else:
				fullquery = errorq+prompt
		elif answer in 'help ?'.split():
			fullquery = options+prompt
		else:
			if answer in "add_human add_computer".split():
				is_human = (answer == 'add_human')
				
				if add_player_menu(is_human):
					from sabacc.back.Game import players_in_game
					
					if players_in_game != 1:
						player_s = 's'
					else:
						player_s = ''
					query = 'Player successfully added. ' + str(players_in_game) + ' player' + player_s + ' now in game.\n'
					
					# Add options if necessary
					if players_in_game == 1:
						validoptions.append('remove')
						# Instructions + add + remove + help/quit
						options = optionslist[0] + optionslist[1] + optionslist[2] + optionslist[4]
					elif players_in_game == 2:
						validoptions.append('start')
						# Instructions + add + remove + start + help/quit
						options = optionslist[0] + optionslist[1] + optionslist[2] + optionslist[3] + optionslist[4]
				else:
					query = 'Player not added!\n'
			elif answer == "remove":
				if remove_player_menu():
					from sabacc.back.Game import players_in_game
					
					if players_in_game != 1:
						player_s = 's'
					else:
						player_s = ''
					query = 'Player successfully removed. ' + str(players_in_game) + ' player' + player_s + ' now in game.\n'
					
					# Remove options if necessary
					if players_in_game == 1:
						validoptions.remove('start')
						# Instructions + add + remove + help/quit
						options = optionslist[0] + optionslist[1] + optionslist[2] + optionslist[4]
					elif players_in_game == 0:
						validoptions.remove('remove')
						# Instructions + add + help/quit
						options = optionslist[0] + optionslist[1] + optionslist[4]
				else:
					query = 'Player not removed!\n'
			elif answer == "start":
				if start_game_menu():
					query = 'Game over! What do you want to do now?\n'
				else:
					query = ''
			elif answer == "show":
				from sabacc.back.Game import sabacc_pot, names
					
				if len(names) == 0:
					print 'There are no players in the game.'
				elif len(names) == 1:
					print 'Player %s is in the game.' %names[0]
				else:
					print 'Players %s are in the game.' %names
				
				print 'There are %s credits in the Sabacc pot.' %sabacc_pot
				
				query = 'What do you want to do now?\n'
			else: # quit
				from sabacc.back.Game import reset
				
				if not reset():
					raise SystemExit('Error resetting game variables! Quitting...\n')
				break
			fullquery = query+options+prompt

def add_player_menu(is_human):
	'''Gets player name & details and adds to the game'''
	
	if is_human:
		query = "What is your name? (CTRL-C to abort) "
	
	while True:
		answer = ''
		if is_human:
			try:
				answer=raw_input(query)
				print
			except EOFError:
				pass
			except KeyboardInterrupt:
				print
				return False
		else:
			# Get filename from other method
			answer = get_filename()
			
			if not answer: # CTRL-C or other error
				return False
		
		if answer != "":
			from sabacc.back.Game import add_player
			
			if is_human:
				interface = playerInterface(answer)
			else:
				interface = None
			
			if add_player(answer, interface, is_human):
				global humans_in_game
				humans_in_game += is_human
				return True
	
def remove_player_menu():
	'''Gets player name and removes from the game'''
	
	query = "Please enter the name of the player to remove.\n"
	query += "Players in game:\n"
	
	from sabacc.back.Game import names
	for name in names:
		query += "\t%s\n" %name
	
	query += "\nOr press CTRL-C to abort."
	prompt = "> "
	print query
	
	while True:
		answer = None
		try:
			answer=raw_input(prompt)
			print
		except EOFError:
			pass
		except KeyboardInterrupt:
			print
			return False
		
		if answer != "":
			from sabacc.back.Game import names, loaded, remove_player
			
			# Get player object
			if answer in names:
				player = loaded[names.index(answer)][0]
			else:
				player = None
			
			if remove_player(answer):
				from sabacc.back.Agents import HumanAgent
				if type(player) == HumanAgent:
					global humans_in_game
					humans_in_game -= 1
				
				return True
			else:
				print "Player %s not removed!" %answer
def start_game_menu():
	'''Prompts user for initial ante, then starts the game.'''
	
	query = "Please enter initial ante (CTRL-C to abort) "
	
	while True:
		answer = None
		try:
			answer=raw_input(query)
			print
		except EOFError:
			pass
		except KeyboardInterrupt:
			print
			return False
		
		if answer != "":
			try:
				answer = int(answer)
			except ValueError:
				print errorq
				answer = ''
		
		if type(answer) == int:
			global humans_in_game
			from sabacc.back import Game
			
			Game.interface=gameInterface()
			
			if Game.start_game(answer):
				return True
			else:
				return False

def agent_menu():
	'''Prompts the user whether to create a new agent or view/modify an existing one.'''
	
	query = "Welcome to the Sabacc Agent Interface\n"
	options = """\nPlease choose from the following:
	new:	Create a new agent
	load:	Load an existing agent to view or modify
	help:	Display this screen
	quit:	Return to the main menu
"""
	validoptions = 'new load help quit ?'.split()
	
	prompt = "> "
	fullquery = query+options+prompt
	
	while True:
		answer = None
		try:
			answer=raw_input(fullquery)
		except EOFError:
			print
			answer = "quit"
		
		# Keep asking until a valid answer is given
		if answer not in validoptions:
			if answer == "":
				fullquery = prompt
			else:
				fullquery = errorq+prompt
		elif answer in 'help ?'.split():
			fullquery = options+prompt
		else:
			if answer == 'new':
				if new_agent_menu():
					query = 'New agent successfully created.\n'
				else:
					query = 'Create new agent failed!\n'
			elif answer == "load":
				load_agent_menu()
				query = ''
			else: # quit
				break
			fullquery = query+options+prompt

def get_filename(save=False):
	'''Gets an agent filename from the user'''
	from settings import agent_dir
	import os.path
	
	current_dir = agent_dir
	relative_dir = 'agents'
	dirs, files = get_dir_contents(current_dir)
	
	if save:
		options = 'Please enter a filename or a directory to save into or press CTRL-C to cancel:\n> '
	else:
		options = 'Please choose a file or a directory or press CTRL-C to cancel: '
	update_listing = True
	
	while True:
		if update_listing:
			update_listing = False
			if len(dirs) == 1:
				diry = 'y'
			else:
				diry = 'ies'
			if len(files) == 1:
				filey = ''
			else:
				filey = 's'
			
			query = "Current directory is '%(current)s'. %(dir)s director%(diry)s and %(file)s file%(filey)s found:\n\n" \
				%{'current':relative_dir, 'dir':len(dirs), 'diry':diry, 'file':len(files), 'filey':filey}
			
			dirdisplay = ''
			if len(dirs) >= 1:
				count = 0
				for dir in dirs:
					# No more than 4 entries per line
					if count  == 4:
						count = 0
						tab_or_newline = '\n'
					else:
						tab_or_newline = '\t'
					
					dirdisplay += '[%s]' %dir + tab_or_newline 
					count += 1
				dirdisplay += '\n'
			count = 0
			for file in files:
				# No more than 4 entries per line
				if count  == 3:
					tab_or_newline = '\n'
					count = -1
				else:
					tab_or_newline = '\t'
				
				dirdisplay += file + tab_or_newline
				count += 1
			dirdisplay += '\n'
			fullquery = query + dirdisplay + options
		
		answer = ""
		
		try:
			answer=raw_input(fullquery)
			print
		except EOFError:
			pass
		except KeyboardInterrupt:
			print
			return False
		
		# Keep asking until a valid answer is given
		if not save and answer not in files + dirs:
			if answer == "":
				fullquery = options
			else:
				fullquery = errorq+options
		elif answer in dirs:
			current_dir = os.path.abspath(os.path.join(current_dir, answer))
			dirs, files = get_dir_contents(current_dir)
			update_listing = True
			
			if answer == '..':
				relative_dir = previous_dir
			else:
				previous_dir = relative_dir
				relative_dir += '/%s' %answer
		elif save:
			if '.' not in answer:
				answer += '.xml'
			
			save_file = True
			from string import lower
			
			if lower(answer[-4:]) != '.xml':
				print "Selected filename does not have the .xml file extension."
				xmlquery = "Do you want it to be added? (yes/no) "
				
				add_xml_extension = None
				while add_xml_extension == None:
					try:
						add_xml_extension=raw_input(xmlquery)
					except EOFError:
						pass
					except KeyboardInterrupt:
						print
						save_file = False
						break
					if add_xml_extension not in ['yes', 'no']:
						add_xml_extension = None
						
				if add_xml_extension == 'yes':
					answer += '.xml'
					
			if answer in files: # if file exists
				print "Selected file already exists."
				xmlquery = "Do you want to overwrite? (yes/no) "
				
				overwrite_file = None
				while overwrite_file == None:
					try:
						overwrite_file=raw_input(xmlquery)
					except EOFError:
						pass
					except KeyboardInterrupt:
						print
						save_file = False
						break
					if overwrite_file not in ['yes', 'no']:
						overwrite_file = None
				
				if overwrite_file == 'no':
					save_file = False
			
			if save_file:
				return answer
			
		else: #load file 
			return os.path.join(current_dir, answer)
		

def get_dir_contents(directory):
	import os
	from string import lower
	from settings import agent_dir
	
	os.chdir(directory)
	dirs = filter(os.path.isdir, os.listdir('.'))
	files = filter(os.path.isfile, os.listdir('.'))
	
	# Allow user to go back to previous dir, but not go above agent dir
	if os.path.abspath(directory) != os.path.abspath(agent_dir):
		dirs.insert(0, '..')
	
	# XML files only!
	xmlfiles = []
	for file in files:
		if lower(file[-4:]) == '.xml':
			xmlfiles.append(file)
	files = xmlfiles
	
	return dirs, files

def new_agent_menu():
	'''Prompt for name and other details, then save agent in specified location.'''
	
	query = "Please enter a name, or press CTRL-C to abort: "
	
	from settings import rulesets
	name = None
	ruleset = None
	
	while True:
		answer = None
		errors = False
		
		try:
			answer=raw_input(query)
			print
		except EOFError:
			print
			answer = ''
		except KeyboardInterrupt:
			print
			return False
		
		if answer != "":
			if name == None:
				name = answer
				query = '''Please choose a rule set, or press CTRL-C to abort:
(This may be one of %s) ''' %rulesets
			elif answer in rulesets:
				ruleset = answer
			else:
				sys.stderr.write("Error: '%s' is not a valid option!\n" % answer)
				
			if ruleset:
				from tempfile import mkstemp
				from sabacc.back import xml_tools
				
				filename = mkstemp('.xml', 'sabacc_', text=True)[1]
				
				from os import remove
				
				if not xml_tools.create_agent(filename, name, ruleset):
					sys.stderr.write("Error creating temporary file!\n")
					remove(filename)
					return False
				
				from sabacc.back.Agents import RuleBasedAgent
				agent = RuleBasedAgent(filename)
				
				if agent.loaded:
					final = modify_agent(agent, new_file=True)
				else:
					final = False
				remove(filename) # delete temp file
				
				return final
	
def load_agent_menu():
	'''Loads an agent from a file'''
	agent_file = get_filename()
	
	if not agent_file:
		return False
	
	from sabacc.back.Agents import RuleBasedAgent
	agent = RuleBasedAgent(agent_file)
	
	if not agent.loaded:
		return False
	
	final = modify_agent(agent)
	return final
		
def modify_agent(agent, new_file=False):
	'''Show details of an XML agent and allow them to be
	modified and the file saved.'''
	
	stats = agent.stats.copy()
	
	options1 = """\nPlease choose from the following:
	ruleset:	Change agent ruleset"""
	oprevert = """
	revert:		Revert to saved version of agent"""
	opsave = """
	save:		Save this agent"""
	options2 = """
	help:		Display this screen
	quit:		Return to the agent menu
"""
	validoptions = 'ruleset help quit ?'.split()
	
	if new_file:
		validoptions.append('save')
		options = options1 + opsave + options2
	else:
		options = options1 + options2
	
	prompt = "> "
	
	while True:
		stats.update(name=agent.name, ruleset=agent.ruleset)
		
		query = '''Editing agent '%(name)s'. Agent rule set is '%(ruleset)s'.
General status of agent %(name)s:
	Wins: %(wins)i
	Losses: %(losses)i
	Pure Sabaccs: %(pure_sabaccs)i
	Bomb Outs: %(bomb_outs)i\n''' %stats
		fullquery = query+options+prompt
		
		errors = False
		answer = None
		try:
			answer=raw_input(fullquery)
		except EOFError:
			print
			answer = "quit"
		
		# Keep asking until a valid answer is given
		if answer not in validoptions:
			if answer == "":
				fullquery = prompt
			else:
				fullquery = errorq+prompt
		elif answer in 'help ?'.split():
			fullquery = options+prompt
		else:
			if answer == 'ruleset':
				new_ruleset = modify_agent_ruleset(agent.ruleset)
				
				if new_ruleset and new_ruleset != agent.ruleset:
					agent.ruleset = new_ruleset
					
					# Add option to save if it wasn't there already
					if  'save' not in validoptions:
						validoptions.append('revert')
						validoptions.append('save')
						options = options1 + oprevert + opsave + options2
			
			elif answer in ['revert', 'save']:
				if answer == 'save':
					if new_file:
						orig_filename = agent.filename
						filename = get_filename(save=True)
						
						if not filename:
							errors = True
						else:
							from shutil import copy
							try:
								copy(orig_filename, filename)
								agent.filename = filename
								
								new_file = False
							except IOError:
								sys.stderr.write('Error writing file to XML!\n')
								errors = True
						
					if not errors and not agent.save_to_xml():
						errors = True
				else: # revert
					if not agent.load_from_xml():
						errors = True
				
				if not errors:
					if 'revert' in validoptions:
						validoptions.remove('revert')
					validoptions.remove('save')
					options = options1 + options2
					
					if answer == 'save':
						print "File saved OK."
					else:
						print "Successfully reverted to previous save."
				
			else: # quit
				break
	
	return False

def modify_agent_ruleset(ruleset):
	'''Prompt for new rule set, then return.'''
	
	from settings import rulesets
	query = '''Your current rule set is '%s'.
Please choose a new one or press CTRL-C to abort:
(This may be one of %s) ''' %(ruleset, rulesets)
	
	while True:
		answer = None
		errors = False
		
		try:
			answer=raw_input(query)
			print
		except EOFError:
			print
			answer = ''
		except KeyboardInterrupt:
			print
			return
		
		if answer != "":
			if answer in rulesets:
				return answer
			else:
				sys.stderr.write("Error: '%s' is not a valid option!\n" % answer)
