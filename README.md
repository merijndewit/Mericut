# Mericut GitHub page information

  
![](https://lh5.googleusercontent.com/67m39O05kiG_hSGt6J7HhXVSXeK1PaFPQQN3faKrRFlyukiX2zkZ0uIwM6Y7X5NtHOKDQK4gfiyLAaX435-YuNXK_gHhaR_DAE0C1D5CbOgE45VHy-DJRvbL4LK00xdr5KvPcQ0g2nYexJzey0G_aw4)

## Introduction

Mericut is an open source cutting/drawing machine that you can build/use at home! Some of you might be familiar with a CriCut machine which this project is inspired from. Mericut can cut and draw on various materials like paper, cardboard, leather, fabric and much more. You can control it with a custom program for easy use. In this program you can draw by clicking and dragging on a canvas or simply import an svg found on the internet or made in another program. When you have the canvas exactly how you want you can make the machine do all the work and let it cut or draw it onto a surface by simply pressing onto a button.

  

### The hardware

To build the hardware you need to have a 3d printer and some general knowledge about electronics.

  

#### Part list

-   608ZZ011 bearings (x16)
    
-   MR84ZZ bearings(2x)
    
-   LM8UU (x5)
    
-   Nema 17 stepper motor with a height of 20 mm (2x)
    
-   Nema 17 stepper motor with a height of ~40 mm (3x)
    
-   8mm diameter rod with 350mm length (6x)
    
-   8mm diameter rod with ~100mm length (2x)
    
-   25mm springs with 8mm diameter (4-6x) (the amount depends on the strength of the springs)
    
-   24mm diameter 350mm length wooden stick like a broomhandle (2x)
    
-   ~300 grams of pla or comparable type of filament
    
-   Nema 17 gt2 belt pulley (1x)
    
-   Gt2 belt (~1 metre)
    
-   Microcontroller like arduino uno/esp32
    
-   Steppermotor drivers like DRV8825
    
-   Power Supply ~12v for driving the stepper motors
    

  
![](https://lh3.googleusercontent.com/1L8uiIdaErew6F5wLnHapGqDGk_n7mzV2tGm9sOQa2gdpV-6gLDGQYIIND4VtbdSBYPyYjsyLgVhYTi3oXfSGEpRpZq10ZgLLMicV4h08TYaLZqRLz7KPjmf5DavUiLQR8_6s97uGyx8cE-WO-xKkP8)

In the repository is a freecad file with all the models that are needed to build it. By importing the file into FreeCad you can export all the needed models as your desired filetype. You can also modify all the models to make them perfectly fit with the hardware you have or to improve/add components.

  
  
  
  

For the electronics you can create your own shield for the microcontroller with the stepper motor drivers. ![](https://lh5.googleusercontent.com/lDItHYfeKUwyWcLIa-HCWOj2HMokKBSnUKjw_Hd_oro7VppDhFV4eowlnBR0y33VXeyPadnM6KwRBWx1QZwXW0BHl7lMrwWKSqh5Imb3OsqAcTFByR2zFZqba_ESplXNT1nJn4cmPTMSZ0fGNDXouds)![](https://lh3.googleusercontent.com/GWuagMZ0Vlq6J-R6Q-_FPN73gNQed0uZ6P69m9ZdX_RthHgC-WIfb_MQG3lVXZqUbKnMQcj-1dVuTBk9plaTmjm1XT73kp0W6FfJecarvaVyo9fkP3wYzf47Zzdo7QTBMKzD9rjPpmQ52Kp7pG3wlEM)

  

(Build Instructions and wiring diagram are coming in the future)

  
  
  
  
  
  
  
  
  
  
  
  

## The Software![](https://lh6.googleusercontent.com/ZoEBiYZkYSWtisNVgERJ-fcdHCrXStmFIsCwzcU-mzmS4DENVPGzrxp4FtyTn1lsTCwPDqA4U6mv6U4IgAms7p_b3y_u5jhnoFS-AHGx4TzSb1OICRc7GSd-8a9OwuljGwlpgoeUkurHRJJQHaWMTKc)

## Pc program

Mericut has an easy to use GUI (graphical user interface) that is used to make drawings, import svg’s and to send commands to the machine.

  

### Preview

The program can show you what your drawing/cutout is gonna look like. You also have backgrounds you can set that have different “a paper” sizes to help you see if the drawing/cutout will fit on the material you use.
