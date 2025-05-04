---
title: "Semi-Autonomous Quadcopter Part 1"
date: 2018-07-08
coverImage: "untitled-50-3.jpg"
---

## Background

Ever since I did a line following collision avoidance Arduino robot project at university, I liked the idea of applying this to an indoor quadcopter. This is quite an ambitious project and I am fully prepared not to completely realize the goal but I would like to see how far I can get!

## Goal

Create a semi-autonomous quadcopter that will take off, fly around avoiding obstacles, land and re-charge without human intervention.

## Stages

1\. Acquire cheap quadcopter to master flying skills and understand basic operations. 2. Research and order parts for a quadcopter suitable for indoor flight. 3. Build quadcopter, wire up electronics and calibrate, and design and 3D print propeller guards for indoor use. 4. Design frame and 3D print for improved resilience indoors and custom sensor mounts. 5. Interface sensors for collision avoidance. 6. Test, test, test, and iterate. 7. Develop take-off and landing system in indoor environments. 8. Test, test,test. 9. Create concepts for automatic recharging. 10. Combine and test.

## Stage 1 - 3:

I bought a cheap quadcopter on Amazon from China. It never arrived. Not dissuaded by this, I bought the same one from a UK seller which arrived the next day. It didn't take too long to learn the basics of "Mode 2" flight control and practiced flying it indoors and landing it on small items of furniture.

Next, I did some research on DIY quadcopter forums and came to the conclusion that 150mm was about as big as I could go for indoor use.

After finding a 150mm quadcopter frame on bangood which came with a power distribution board, I sourced the motors, electronic speed controllers, propellers, receiver, battery and flight controller that were suitable for the frame size. I decided to go for a relatively cheap radio transmitter and receiver to start me off.

\[caption id="attachment\_98" width="600" align="aligncenter"\]![untitled.50 (3)](images/untitled-50-3.jpg) Render of Quadcopter and propeller guards\[/caption\]

After waiting around 3 weeks for all of the components to arrive, I assembled the mechanical parts together and created a 3D model of the quadcopter. I then designed propeller guards around the 3D model to stop the quadcopter from causing too much damage indoors.

\[caption id="attachment\_127" width="600" align="aligncenter"\]![IMG_20171129_123017](images/img_20171129_123017.jpg) ESCs soldered to Motors and PDB\[/caption\]

After soldering the ESCs to the motors and PDB, I connected up the ESC cables to the NAZE 32 flight controller to test everything worked correctly. After many failed attempts to try and calibrate the ESCs, it turned out the issue was that the voltage regulator from the PDB and the voltage regulator from one of the ESCs were interfering with eachother. After disconnecting the power cable to the flight controller, everything was calibrated and I got the motors responding to the transmitter.

I then shortened and re-soldered all of the wires and assembled the frame and the propellers. I positioned the battery so the centre of gravity was as close to the middle as possible and used some velcro and double sided tape to secure it.

It was time for its maiden flight!

(INSERT GIF HERE)

It worked!

![](images/img_20180324_161943.jpg)

The propeller guards broke immediately on a hard impact against the table and then the floor. I am not sure whether their material and current geometry will be up to scratch against any hard impacts.

\[caption width="4160"\]![](images/img_20180329_203555.jpg)Quadcopter with new and improved propeller guards\[/caption\]

I then redesigned and re-printed the 4 propeller guards to reduce the stress raisers found on the initial design at their fracture points and mounted them to the bottom of the frame to ensure the motors are on more of a flat surface and to provide plastic feet for landing.
