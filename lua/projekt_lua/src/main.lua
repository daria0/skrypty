---
--- Created by Daria Siemieniuk
--- project: SPACE INVADERS USING LUA & LOVE
---


--- CONFIG:
RELOAD_TIME = 20
--- PLAYER
PLAYER_X = 0
PLAYER_Y = 570
PLAYER_WIDTH = 22
PLAYER_HEIGHT = 22
PLAYER_SPEED = 5
--- BULLET
BULLET_WIDTH = 4
BULLET_HEIGHT = 8
--- ENEMY
ENEMY_X = 0
ENEMY_Y = 0
ENEMY_WIDTH = 28
ENEMY_HEIGHT = 20
ENEMY_SPEED = 1
NUMBER_OF_ENEMIES = 20
NUMBER_OF_ROWS = 5

--in case of changing scale of the images:
love.graphics.setDefaultFilter("nearest", "nearest")

enemy = {}
enemies_controller = {}
enemies_controller.enemies = {}
enemies_controller.image = love.graphics.newImage("enemy.png")
bullet_image = love.graphics.newImage("bullet.png")
enemy_killed_sound = love.audio.newSource("invaderkilled.wav", "static")

function love.load()
    player = {}
    player.x = PLAYER_X
    player.y = PLAYER_Y
    player.image = love.graphics.newImage("player.png")
    player.bullets = {}
    player.reload_time = RELOAD_TIME
    player.fire_sound = love.audio.newSource("shoot.wav", "static")
    player.fire = function()
        if player.reload_time <= 0 then
            love.audio.play(player.fire_sound)
            player.reload_time = RELOAD_TIME
            bullet = {}
            bullet.x = player.x + PLAYER_WIDTH / 2 - BULLET_WIDTH / 2
            bullet.y = player.y
            table.insert(player.bullets, bullet)
        end
    end
    for i =0, NUMBER_OF_ROWS do
        for j=0, NUMBER_OF_ENEMIES/NUMBER_OF_ROWS do
            enemies_controller:spawnEnemy(j*30, i*30)
        end
    end
end

function enemies_controller:spawnEnemy(x, y)
    enemy = {}
    enemy.x = x
    enemy.y = y
    enemy.bullets = {}
    enemy.reload_time = RELOAD_TIME
    table.insert(self.enemies, enemy)
end

function enemy:fire()
    if self.reload_time <= 0 then
        self.reload_time = RELOAD_TIME
        bullet = {}
        bullet.x = self.x + ENEMY_WIDTH / 2 - BULLET_WIDTH / 2
        bullet.y = self.y
        table.insert(self.bullets, bullet)
    end
end

function detectCollisions(enemies, bullets)
    for i, enemy in pairs(enemies) do
        for j, bullet in pairs(bullets) do
            if bullet.y <= enemy.y + ENEMY_HEIGHT and bullet.x > enemy.x and bullet.x < enemy.x + ENEMY_WIDTH then
                print("INVADER KILLED!")
                table.remove(enemies, i)
                table.remove(player.bullets, j)
                love.audio.play(enemy_killed_sound)
            end
        end
    end
end

function love.update(dt)
    player.reload_time = player.reload_time - 1
    if love.keyboard.isDown("left") then
        player.x = player.x - PLAYER_SPEED
    elseif love.keyboard.isDown("right") then
        player.x = player.x + PLAYER_SPEED
    end

    if love.keyboard.isDown("space") then
        player.fire()
    end

    for i, bullet in pairs(player.bullets) do
        if bullet.y < -10 then
            table.remove(player.bullets, i)
        end
        bullet.y = bullet.y - 10
    end

    for _, enemy in pairs(enemies_controller.enemies) do
        enemy.y = enemy.y + ENEMY_SPEED
    end

    detectCollisions(enemies_controller.enemies, player.bullets)
end

function love.draw()
    --love.graphics.print("Hello World!", 100, 100)

    love.graphics.draw(player.image, player.x, player.y)

    for _, enemy in pairs(enemies_controller.enemies) do
        love.graphics.draw(enemies_controller.image, enemy.x, enemy.y)
    end

    for _, bullet in pairs(player.bullets) do
        --love.graphics.rectangle("fill", bullet.x, bullet.y, BULLET_WIDTH, BULLET_HEIGHT)
        love.graphics.draw(bullet_image, bullet.x, bullet.y)
    end
end