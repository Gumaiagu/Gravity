# Gravity

This program simulates the real-life gravity of massive objects.

## Executing

To use this program, you'll need a Python 3 virtual environment with the Pygame and Numpy libraries.

```
python3 -m venv .venv
source .venv/bin/activate
pip3 install pygame numpy
```

## Mathematical implementations

This program uses the Newtonian model of gravity.

Originally, Newton's formula for gravity was `-G*(m1*m2)/r²`, but we need to multiply that by the displacement vector to get the force vector. The formula for that is `(p1-p2)/r`. I simplified the formula to `-G*m1*m2*(p1-p2)/r³`, which appears on Wikipedia's page for Newton's universal law of gravitation. Finally, I simplified the m1 term with the mass that appears in the "force to acceleration" formula, also created by Newton (f/m=a), giving the following calculations: 

```python
f = 0
for object in objects_in_scene:
  f -= G * object.mass * (self.position - object.position) / distance(self.position, object.position)**3
  self.velocity = self.velocity + f
  self.position = self.position + self.velocity
```

This simulation was made using differential equations, which made the simulation less than completely realistic but able to simulate more than two objects (because humanity has not yet solved the three-body problem). However, it's realistic enough to be a cool project to show in a physics class.

## Cool observations

Initially, I thought there was a bug, but it's actually a cool fact about reference points. When using the center of the screen as the reference point, binary systems appeared to "shift" over time, which is different from what we learn in school and see in most videos on the internet, where both objects orbit the center of mass of the system. After some searching, I found that other Newtonian simulations on the internet exhibited the same "bug" that I had noticed. After testing, I discovered that the model we see in school uses the center of mass as the reference point. 

I did the same, and the center of mass of the system was always in the center of the screen, making the simulation look like the ones we usually watch.

## Changing parameters

To create custom objects, go to the "main" function and change the "Objects" created and added to the "objects_in_scene" list. I know changing the code to make these kinds of customizations is not the best practice, but making you write all the simulation options in the command line would be even worse. I didn't want to spend the rest of my school break on this project just to create a UI alternative.
