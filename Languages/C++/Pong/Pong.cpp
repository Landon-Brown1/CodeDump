#include <SFML/Graphics.hpp>
#include <SFML/Window.hpp>
#include <SFML/System.hpp>
#include <math.h>
#include <iostream>

const int windowWidth = 800;
const int windowHeight = 600;
using namespace sf;

class Paddle {
public:
    RectangleShape shape;
    float speed = 6.0f;
    bool side = false;

    Paddle(float x,bool y) {
        shape.setSize(Vector2f(10, 100));
        shape.setPosition(Vector2f(x, windowHeight / 2 - shape.getSize().y / 2));
        shape.setFillColor(Color::White);
        side = y;
    }

    void moveUp() {
        if (shape.getPosition().y > 0)
            shape.move(Vector2f(0, -speed));
    }

    void moveDown() {
        if (shape.getPosition().y + shape.getSize().y < windowHeight)
            shape.move(Vector2f(0, speed));
    }

    Vector2f getCenter() const {
        return shape.getPosition() + (shape.getSize() / 2.0f);
    }
};

class Ball {
public:
    CircleShape shape;
    float speedX = -4.0f;
    float speedY = -4.0f;
    bool justBounced = false;
    short timeSinceBounce = 0;
    float ballSpeed = 5.0f; // Constant speed

    Ball() {
        shape.setRadius(10);
        shape.setFillColor(Color::White);
        shape.setPosition(Vector2f(windowWidth / 2, windowHeight / 2));
    }

    void move() {
        shape.move(Vector2f(speedX, speedY));
        if (shape.getPosition().y <= 0 || shape.getPosition().y + shape.getRadius() * 2 >= windowHeight)
            speedY = -speedY;
    }

    void reset() {
        shape.setPosition(Vector2f(windowWidth / 2, windowHeight / 2)); // set ball to middle court
        speedX = speedY = 0; // stop it from moving
    }

    void start() {
        speedX = rand() % 5 + 2;    // random starting angle every round
        speedY = ballSpeed - speedX;
        if (rand() % 2 >= 1)        // sometimes shoot left, sometimes right
            speedX *= -1;
    }

    void update(const Paddle& left, const Paddle& right) {
        timeSinceBounce++;

        if (timeSinceBounce > 3) {
            if (!shape.getGlobalBounds().findIntersection(left.shape.getGlobalBounds()) &&
                !shape.getGlobalBounds().findIntersection(right.shape.getGlobalBounds())) {
                justBounced = false;
            }
        }
    }

    Vector2f getCenter() const {
        return shape.getPosition() + Vector2f(shape.getRadius(), shape.getRadius());
    }   

    void checkCollision(Paddle& paddle) {
        if (!justBounced && shape.getGlobalBounds().findIntersection(paddle.shape.getGlobalBounds())) {
            std::cout << "before SpeedX: " << speedX << ", SpeedY: " << speedY << "\n";
            float relativeIntersect = getCenter().y - paddle.getCenter().y;
            float normalized = std::max(-1.0f, std::min(1.0f, relativeIntersect / 50.0f));
            float maxBounceAngle = 75.0f * (3.141592f / 180.0f);
            float bounceAngle = normalized * maxBounceAngle;

            speedX = ballSpeed * (paddle.side ? 1.0f : -1.0f) * cos(bounceAngle);
            speedY = ballSpeed * sin(bounceAngle);

            justBounced = true;
            timeSinceBounce = 0;
            std::cout << "Bounce angle: " << bounceAngle << "\n";
            std::cout << "after SpeedX: " << speedX << ", SpeedY: " << speedY << "\n";
        }
    }
};

struct Board {
    void draw_game(RenderWindow& w, Paddle lp, Paddle rp, Ball b, Text st, Text rt){
        w.clear();
        w.draw(lp.shape);
        w.draw(rp.shape);
        w.draw(st);
        w.draw(rt);
        w.draw(b.shape);
        w.display();
    }
};

int main() {
    RenderWindow window(VideoMode(Vector2u(windowWidth, windowHeight)), "Pong");
    window.setFramerateLimit(60);

    Board b;
    Paddle leftPaddle(20,true);
    Paddle rightPaddle(windowWidth - 30,false);
    Ball ball;

    // Simple AI for right paddle
    float aiCenterY = rightPaddle.getCenter().y;
    float ballY = ball.getCenter().y;
    float aiSpeed = 3.0f;

    Font font;
    if (!font.openFromFile("assets/fonts/ARIAL.ttf")) {
        std::printf("Failed to load font ARIAL\n") ;
        return -1; // Exit if font can't be loaded
    }
    
    int leftScore = 0, rightScore = 0;
    Text scoreText(font, "", 30);
    Text readyText(font, "", 30);
    scoreText.setFillColor(Color::White);
    readyText.setFillColor(Color::Black);
    readyText.setString("Ready?");
    auto bounds = readyText.getGlobalBounds();
    readyText.setPosition(Vector2f(windowWidth / 2.f - bounds.size.x / 2.f, 50.0f));
    bool waitingToStart = false;
    Clock waitClock;
    
    while (window.isOpen()) {
        while (auto eventOpt = window.pollEvent()) {
            Event event = *eventOpt;
            if (event.is<sf::Event::Closed>())
                window.close();
        }

        // Controls
        if (Keyboard::isKeyPressed(Keyboard::Key::W))
            leftPaddle.moveUp();
        if (Keyboard::isKeyPressed(Keyboard::Key::S))
            leftPaddle.moveDown();
        // if (Keyboard::isKeyPressed(Keyboard::Key::Up))
        //     rightPaddle.moveUp();
        // if (Keyboard::isKeyPressed(Keyboard::Key::Down))
        //     rightPaddle.moveDown();
        
        // Move ball
        if (waitingToStart) {
            // Draw "Ready?" and wait
            if (waitClock.getElapsedTime().asSeconds() >= 3.0f) {
                waitingToStart = false;
                readyText.setFillColor(Color::Black);
                ball.start(); // now it starts moving
            }
        } else {
            // Normal gameplay
            ball.move();
            ball.update(leftPaddle, rightPaddle);
            ball.checkCollision(leftPaddle);
            ball.checkCollision(rightPaddle);
        }
        

        // Computer player
        aiCenterY = rightPaddle.getCenter().y;
        ballY = ball.getCenter().y;
        if (std::abs(ballY - aiCenterY) > 5) {
            if (ballY < aiCenterY && rightPaddle.shape.getPosition().y > 0)
                rightPaddle.shape.move(Vector2f(0, -aiSpeed));
            else if (ballY > aiCenterY && rightPaddle.shape.getPosition().y + rightPaddle.shape.getSize().y < windowHeight)
                rightPaddle.shape.move(Vector2f(0, aiSpeed));
        }
        
        // Score check
        if (ball.shape.getPosition().x < 0) {
            rightScore++;
            ball.reset();
            // Update score text
            scoreText.setString(std::to_string(leftScore) + " : " + std::to_string(rightScore));
            auto bounds = scoreText.getGlobalBounds();
            scoreText.setPosition(Vector2f(windowWidth / 2.f - bounds.size.x / 2.f, 10.f));
            // Start next round
            readyText.setFillColor(Color::White);
            waitingToStart = true;
            waitClock.restart();
        }
        if (ball.shape.getPosition().x > windowWidth) {
            leftScore++;
            ball.reset();
            // Update score text
            scoreText.setString(std::to_string(leftScore) + " : " + std::to_string(rightScore));
            auto bounds = scoreText.getGlobalBounds();
            scoreText.setPosition(Vector2f(windowWidth / 2.f - bounds.size.x / 2.f, 10.f));
            // Start next round
            readyText.setFillColor(Color::White);
            waitingToStart = true;
            waitClock.restart();
        }

        // Render
        b.draw_game(window, leftPaddle, rightPaddle, ball, scoreText, readyText);
    }

    return 0;
}