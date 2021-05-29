---
--- Generated by EmmyLua(https://github.com/EmmyLua)
--- Created by daria.
--- DateTime: 29.05.2021 00:01
---


--- CONFIG:
RELOAD_TIME = 20
--- PLAYER
PLAYER_X = 0
PLAYER_Y = 570
PLAYER_WIDTH = 80
PLAYER_HEIGHT = 20
PLAYER_SPEED = 5
--- BULLET
BULLET_WIDTH = 10
BULLET_HEIGHT = 10
--- ENEMY
ENEMY_X = 0
ENEMY_Y = 0
ENEMY_WIDTH = 80
ENEMY_HEIGHT = 20
ENEMY_SPEED = 5

enemy = {}
enemies_controller = {}
enemies_controller.enemies = {}

function love.load()
    player = {}
    player.x = PLAYER_X
    player.y = PLAYER_Y
    player.bullets = {}
    player.reload_time = RELOAD_TIME
    player.fire = function()
        if player.reload_time <= 0 then
            player.reload_time = RELOAD_TIME
            bullet = {}
            bullet.x = player.x + PLAYER_WIDTH / 2 - BULLET_WIDTH / 2
            bullet.y = player.y
            table.insert(player.bullets, bullet)
        end
    end
    enemies_controller:spawnEnemy()
end

function enemies_controller:spawnEnemy()
    enemy = {}
    enemy.x = ENEMY_X
    enemy.y = ENEMY_Y
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
end

function love.draw()
    love.graphics.print("Hello World!", 100, 100)
    love.graphics.rectangle("fill", player.x, player.y, PLAYER_WIDTH, PLAYER_HEIGHT)

    for _, enemy in pairs(enemies_controller.enemies) do
        love.graphics.rectangle("fill", enemy.x, enemy.y, ENEMY_WIDTH, ENEMY_HEIGHT)
    end

    for _, bullet in pairs(player.bullets) do
        love.graphics.rectangle("fill", bullet.x, bullet.y, BULLET_WIDTH, BULLET_HEIGHT)
    end
end