
#include "jelloMesh.h"
//
//  main.cpp
//  ikGPU
//
//  Created by Max Gilbert on 1/6/14.
//  Copyright (c) 2014 MaxGilbertCo. All rights reserved.
//
#include <iostream>
#include <fstream>
#include <cmath>
#define PI 3.14
int main(int argc, const char * argv[])
{
    //Positon
    //Length of free joint:
    //float a1 = 1.0;
    
    //Length of two arms
    float a2 = 3.0;
    float a3 = 5.0;
    
    //Desired positon
    float X = 1;
    float Y = 5;
    float Z = 3;
    
    //Transfer to Maya coordinates
    //X=Y
    //Y=Z
    //Z=X
    
    //Initialize thetas
    float theta1 = 0.0;
    float theta2 = 0.0;
    float theta3 = 0.0;
    
    //Find first 3 joint angles according to section 5.2.1 in paper
    theta1 = atan2(Y,X);
    float X1 = Y/sin(theta1);
    float Y1 = Z;
    float numerator =(a2+a3)*(a2+a3)-(X1*X1+Y1*Y1);
    float denominator =(X1*X1+Y1*Y1)-(a2-a3)*(a2-a3);
    numerator = sqrtf(numerator);
    denominator = sqrtf(denominator);
    
    theta3 = atan2(numerator,denominator);
    theta3 *= 2.0f;
    theta2 = atan2(Y1, X1)-atan2(a3*sin(theta3), a2+a3*cos(theta3));
    theta3 = theta3-PI/2;
    
    //Find last three joing angles according to section 5.3
    //R36 = (R03)T*R06
    //Find R03
    
    //Desired rotation
    float thetaX =PI*0/180.0;
    float thetaY =PI*0/180.0;
    float thetaZ =PI*0/180.0;
    float S1 = sinf(thetaX);
    float S2 = sinf(thetaY);
    float S3 = sinf(thetaZ);
    float C1 = cosf(thetaX);
    float C2 = cosf(thetaY);
    float C3 = cosf(thetaZ);
    
    //Create rotation matrices of based off the desired orientation
    glm::mat3 R1 = glm::mat3(glm::vec3(1.0f,0.0f,0.0f),
                             glm::vec3(0.0f,C1,-S1),
                             glm::vec3(0.0f,S1,C1));
    
    glm::mat3 R2 = glm::mat3(glm::vec3(C2,0.0f,-S2),
                             glm::vec3(0.0f,1.0f,0.0f),
                             glm::vec3(S2,0.0f,C2));
    
    glm::mat3 R3 = glm::mat3(glm::vec3(C3,-S3,0.0f),
                             glm::vec3(S3,C3,0.0f),
                             glm::vec3(0.0f,0.0f,1.0f));
    
    
    glm::mat3 R = R1*R2*R3;
    
    //For now just test with desired orientation as identity matrix
    R = glm::mat3();
    
    
    
    //Find R03 by creating rotation matrices from theta1, theta2, and theta3,
    //the first three joint rotations:
    
    //R01 = [c  0  s]
    //      [s  0 -c]
    //      [0  1  0]
    //
    //Unsure about the following 2:
    //R12 = [c  s  0]
    //      [-s c  0]
    //      [0  0  1]
    //
    //R23 = [c  0  s]
    //      [s  0 -c]
    //      [0  1  0]
    
    glm::mat3 R03 = glm::mat3();
    S1 = sinf(theta1);
    S2 = sinf(theta2);
    S3 = sinf(theta3);
    C1 = cosf(theta1);
    C2 = cosf(theta2);
    C3 = cosf(theta3);
    
    glm::mat3 R01 = glm::mat3(glm::vec3(C1,S1,0.0f),
                             glm::vec3(0.0f,0.0f,1.0f),
                             glm::vec3(S1,-C1,0.0f));
    
    glm::mat3 R12 = glm::mat3(glm::vec3(C2,-S2,0.0f),
                             glm::vec3(S2,C2,0.0f),
                             glm::vec3(0.0f,0.0f,1.0f));
    /*
    glm::mat3 R23 = glm::mat3(glm::vec3(C3,-S3,0.0f),
                              glm::vec3(S3,C3,0.0f),
                              glm::vec3(0.0f,0.0f,1.0f));*/
    
    glm::mat3 R23 = glm::mat3(glm::vec3(C3,S3,0.0f),
                              glm::vec3(0.0f,0.0f,1.0f),
                              glm::vec3(S3,-C3,0.0f));

    R03 = R01*R12*R23;
    
    //Find R36 by multiplying transpose of R03 by desired orientation R:
    glm::mat3 R36 =glm::transpose(R03)*R;
    
    //Find thetas 4-6 according to section 5.3
    float theta4 = atanf(-R36[2][1]/-R36[2][0]);
    float sTheta5 = -R36[2][0]*cosf(theta4) - R36[2][1]*sinf(theta4);
    float cTheta5 = R36[2][2];
    float theta5 = atan2f(sTheta5,cTheta5);
    float sTheta6 = -R36[0][0]*sinf(theta4) + R36[0][1]*cosf(theta4);
    float cTheta6 = -R36[1][0]*sinf(theta4) + R36[1][1]*cosf(theta4);
    float theta6 = atan2f(sTheta6,cTheta6);

    //Adjust theta2 and theta3 to Maya coordinate systme
    theta3 = -PI/2-theta3;
    theta2*=-1;
    
    //Adjust thetas4-6 for Maya?
    
    std::cout << "theta1: "<<180*theta1/PI<<"\n";
    std::cout << "theta2: "<<180*theta2/PI<<"\n";
    std::cout << "theta3: "<<180*theta3/PI<<"\n";
    std::cout << "theta4: "<<180*theta4/PI<<"\n";
    std::cout << "theta5: "<<180*theta5/PI<<"\n";
    std::cout << "theta6: "<<180*theta6/PI<<"\n";
    return 0;
}

