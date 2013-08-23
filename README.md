Machine Programmer
=========================


Overview
---------
The goal of this project is to create a program that can program, and explore different AI strategies to do so. When given test cases, it should write a program that can successfully pass all those test cases.


MachineProgrammer is a proof of concept that utilizes genetic algorithms to write working programs in x86 NASM Assembly. The instruction set is simplified for faster evolutions but is just right for writing simple math programs.



**Technologies**  
Client-Side: _jQuery, javascript, JSON_  
Server-Side: _Python, Flask, JSON, Deap, Pusher, Envoy, NASM, gcc-multilib_  



Usage Example
--------------
Let's say we want our machine "programmer" to write a program that multiplies the the first two integers, then add the third integer. Our programmer needs test cases to figure out what kind of output we're looking for. So here we have some simple test cases that cover positive integers, negative integers, and zeros.

| Test Case # | Inputs        | Output       |
|-------------|:-------------:|-------------:|
|      1      | 10, 10, 10    | 110          |
|      2      | -10, -10, -10 | 90           |
|      4      | -10, 10, 10   | -90          |
|      3      | 0, 10, 10     | 10           |


In this prettified interface, we would enter our test cases as thus:

![alt text](https://raw.github.com/evac/MachineProgrammer/master/screenshots/inputs.png "Inputs")



Our programmer will then utilize genetic algorithms to generate programs that it tests against our test cases to see if it meets our requirements. It'll keep going until it finds and outputs a successful assembly program or reaches the max number of generations it can run.

![alt text](https://raw.github.com/evac/MachineProgrammer/master/screenshots/output.png "Output")


Installation
---------------
Will need a 64-bit Linux OS to work right out of the box. Can be adjusted to work on 32-bit Linux though.


```
apt-get install nasm
apt-get install gcc-multilib
```

```
git clone https://github.com/evac/MachineProgrammer.git
cd MachineProgrammer
pip install -r requirements.txt
python run.py
```


You can adjust the evolution settings in the run.py file. The default settings are:  
```
SETTINGS = {
  "population": 100,
  "max_generations": 10,
  "pusher_settings": {
		...
		(Currently uses a free Pusher account I've been using for real-time convenience
			in my demo. You can use your own Pusher keys or, if you don't have an account,
			be sure to make your channel name unique.)
		...
  }
}
```

You can also increase the complexity of the output programs by adding to the assembly instruction set in `/main/asm.py`. Beware that the more complex the problem you're trying to solve or the more numbers of instructions added, the longer it takes to reach a successful solution.


Under the Hood
---------------

###Creating a population of programs
When you click the start button, your inputs are validated, structured and packaged as a chunk of JSON data to the server. Upon receiving the test case inputs, the server will initialize the evolution settings and trigger the birth of many little program instructions. Deap, a genetic algorithm library, is used as the base class for creating our program class with random assembly instructions and operands. Our population is then generated and built out of that default blueprint.

###Evolving codes with the genetic algorithms
We then loop through our population and randomly mutate or mate them to create a new program for the next generation. Our mutating algorithm takes in a single program and randomly shuffles the order of its instructions around. The mating algorithm takes in two programs and cross-breed them by taking parts of one program and parts of another to create a new "offspring" program. And with every generation of new programs, they are sifted through and evaluated for fitness. 

###Compiling and evaluating fitness
Our machine programmer adds its logic to an assembly file that's initialized with the variables and a print call function to output the result. Then it tests the output against our expected output, crossing its bytes for success. If it succeeds, then it can happily stop the evolution process and send the fruit of its success to the client. If it fails then, due to the unique nature of programming problems (further explained in Final Thoughts below), it skips the rest of the test cases and move on to the next experiment.


Final Thoughts
---------------

In progress...