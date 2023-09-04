# this module is all about tracking habits.
# so what functionality must have?
# one can add a habit and a goal.
# They can be ticked off
# they are different types of counters:
# bad habits, good habits, times done the habit, ammount of X needs to be greater than N to tick.
# It must track the date and time of every interaction
## datetime - HabitName - Changedstatus
# information can be retrieved and modified
# Variables:
#Required:name, Type(checkbox, counter, ammount, to_learn, to_ditch), time(dayly, weekly, on_day(1-7), custom)
#optional, to be filled up with time: initiating_motive, values, future_impact_score, percieved_difficulty, criticality_score, Failiure_strategy, reward_ strategy 
# the optional variables will come very usefull, as they will be fed to the llm to give proper advice.
# create habit
# update habit
# delete habit
# check habit
# I suppose that this will require a database perhaps a graph database
# isupose that it will need a habit class and when creating a new habit, it will create another object of it.
# the secondary values are "Unknown by default", but they can have a value with a tag prefix, like GUESS:Indicating that the lmm has valued them, DERIVED:the value has been logically deducted,
# or no tag meaning that user has answered by himself.