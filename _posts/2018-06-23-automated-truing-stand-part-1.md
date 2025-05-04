---
title: "Automated Wheel Truing Stand Part 1"
date: 2018-06-23
tags: 
  - "automation"
coverImage: "ats-prototype-1-41-2-2.jpg"
---

## Background

I used to commute every day to work (~18km) and used heavy panniers on the pothole filled roads of London. After a year with this kind of commute – plus a France cycle tour (~1000km), my rear wheel had had enough. A spoke broke on my cycle tour and I was put in the position of either replacing the wheel or re-truing it.

I opted to buy some new spokes, replace the broken one and re-true it using my frame and brake pads as a guide. This was both not that fun and took quite a bit longer than I would have liked! I’d been thinking about doing a new automation project and an idea popped into my head; what if I could place the wheel in a machine that would do all of this for me and I would never have to worry about re-truing my wheel again? And so the project began.

## Goal

_Create a fully automated bicycle wheel truing stand that will true a wheel with no human intervention._

## Stages:

### Stage 1

- Generate concept designs of the system, create 3D CAD model and build a cheap proof of concept prototype.

### Stage 2

- Wire electronics and write code to enable a semi-automated process with the stand recording how untrue the wheel is and directing the user to tighten the correct spokes in the correct order.

### Stage 3

- Create concepts of automated spoke tightening mechanism and test.

### Stage 4

- Assemble final prototype and amalgamate all aspects of the machine.

## Stage 1

- _Generate concept designs of the system, create 3D CAD model and build a cheap proof of concept prototype._

I realized the system would require a few fundamental features to work:

1. A stiff frame to secure the wheel, preferably positioned in the same way each time.
2. A way of measuring the deflection of the un-true rim.
3. A method of the machine knowing the wheel's position and the position of the spokes.
4. A method of rotating the wheel.
5. A method to tighten each spoke and ensure tension is correct and consistent.

To build a quick and dirty proof of concept prototype, I needed a frame that would both secure the wheel and facilitate the mounting of additional hardware. I found what I thought was a hardwood table of the right size locally on Gumtree and cut a slot out of the middle of it. First mistake. The centre had a single stiffening element but the remainder was just corrugated cardboard rendering the table completely useless as it had lost its stiffness entirely.

\[caption id="attachment\_29" align="aligncenter" width="486"\]![IMG_20180325_155302](images/img_20180325_155302.jpg) Original idea for the frame that didn't work out...\[/caption\]

Luckily, I had a spare 1.76m length of wood (50mm x 50mm cross-section) that was reasonably stiff and would allow me to easily modify the stand and mount hardware. The only issue was that I had a limited length and didn't want to buy more material so I designed the prototype with that in mind.

\[caption id="attachment\_63" align="aligncenter" width="527"\]![ats-prototype-1.41-2 (2)](images/ats-prototype-1-41-2-2.jpg) Rendering of Prototype CAD model\[/caption\]

 

After measuring and modeling my old wheel, I designed a basic frame with the available wood I had and designed brackets that I planned to 3D print. I designed a mount for a spare NEMA 17 stepper motor I had, mounts for the wheel and some angle brackets to keep everything square and make up for my less than perfect hand sawing.

From here, I marked and cut down my length of wood and marked up and drilled the pilot holes for the mounts and brackets.

\[caption id="attachment\_81" align="aligncenter" width="486"\]![IMG_20180616_112635](images/img_20180616_112635.jpg) Sawing wood\[/caption\]

\[caption id="attachment\_82" align="aligncenter" width="486"\]![IMG_20180619_212914](images/img_20180619_212914.jpg) Marking and drilling\[/caption\]

Then I 3D printed the mounts and angle brackets in PETG on my home-built RepRap Prusa i3 3D printer (blog to follow) over the course of a few evenings. I've been using PETG exclusively for a while now and it has been great. It has the strength and rigidity of ABS and it is about as easy to print with as PLA.

\[caption id="attachment\_77" align="aligncenter" width="486"\]![IMG_20180624_153246](images/img_20180624_153246.jpg) 3D printed angle brackets\[/caption\]

I used some cheap wood screws to screw everything together and mounted my old untrue wheel. I immediately realized that I'd based the width of the wheel hub of my front wheel which was 30mm narrower than my rear wheel hub.

\[caption id="attachment\_92" align="aligncenter" width="486"\]![IMG_20180625_221232](images/img_20180625_221232.jpg) First trial fitting\[/caption\]

I then re-designed, 3D printed and fixed the new mounts to the frame which worked great! Although the frame isn't that stiff and won't be suitable for very precise measurements, I'm hoping it will be fine for the proof of concept prototype.

\[caption id="attachment\_108" align="aligncenter" width="486"\]![IMG_20180701_194054](images/img_20180701_1940541.jpg) Stand with motor and wheel\[/caption\]

My initial idea for spinning the wheel was to use the tire as a spring so even if the wheel is a little out of true in the z-direction, the tire can compress as it is being rotated by the roller.

I designed the wheel roller geometry to be similar to a pulley which I thought would most effectively grip the tyre of the wheel from both sides. However, I found that due to how untrue my wheel was, there was either too much pressure when the deflated tyre was deviating to the side, or little to no pressure when the tyre was in the middle of the roller.

\[caption id="attachment\_84" align="aligncenter" width="486"\]![IMG_20180701_194116](images/img_20180701_194116.jpg) The first iteration of the wheel roller\[/caption\]

I tried a simple cylinder instead and reprinted and assembled the roller and found that it worked effectively, with the roller and tyre staying in full contact over an entire revolution. The render below shows the through hole for the motor shaft which I designed with an interference fit, a slot for the captive nut and side hole for a grub screw.

\[caption id="attachment\_101" align="aligncenter" width="486"\]![untitled.52 (2)](images/untitled-52-2.jpg) Wheel roller MK2\[/caption\]

The next [blog post](https://jackchartres.xyz/2018/12/03/automated-wheel-truing-stand-part-2/) on this topic will detail Stage 2 which will include wiring up and mounting the electronics as well as creating a semi-automated wheel truing process.
