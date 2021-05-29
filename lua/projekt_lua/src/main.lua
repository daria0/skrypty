---
--- Created by Daria Siemieniuk
--- project: SPACE INVADERS USING LUA & LOVE
---


--- CONFIG:
RELOAD_TIME = 15
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
ENEMY_SPEED = 0.2
NUMBER_OF_ENEMIES = 20
NUMBER_OF_ROWS = 5
NUMBER_OF_ENEMIES_IN_ONE_ROW = NUMBER_OF_ENEMIES / NUMBER_OF_ROWS

--in case of changing scale of the images:
love.graphics.setDefaultFilter("nearest", "nearest")

enemy = {}
enemies_controller = {}
enemies_controller.enemies = {}
enemies_controller.image = love.graphics.newImage("enemy.png")
bullet_image = love.graphics.newImage("bullet.png")
background_image = love.graphics.newImage("background.png")
enemy_killed_sound = love.audio.newSource("invaderkilled.wav", "static")

function love.load()

    game_over = false
    game_won = false

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

    enemies_width = NUMBER_OF_ENEMIES_IN_ONE_ROW * (ENEMY_WIDTH + 50) - 50
    for i = 0, (NUMBER_OF_ROWS - 1) do
        for j = 0, NUMBER_OF_ENEMIES_IN_ONE_ROW - 1 do
            enemies_controller:spawnEnemy(love.graphics.getWidth() / 2 - enemies_width / 2 + j * 50, i * 50)
        end
    end

    for i, enemy in ipairs(enemies_controller.enemies) do
        if i > (NUMBER_OF_ENEMIES - NUMBER_OF_ENEMIES_IN_ONE_ROW) then
            print(i)
            print(NUMBER_OF_ENEMIES - NUMBER_OF_ENEMIES_IN_ONE_ROW)
            enemy.free_to_shoot = true
        end
    end
end

function enemies_controller:spawnEnemy(x, y)
    enemy = {}
    enemy.x = x
    enemy.y = y
    enemy.bullets = {}
    enemy.reload_time = 10 * RELOAD_TIME
    enemy.free_to_shoot = false
    enemy.fire = function(i)
        if self.enemies[i].reload_time <= 0 and self.enemies[i].free_to_shoot then
            self.enemies[i].reload_time = 10 * RELOAD_TIME
            --if math.random(0, 5) == 1 then
            --shooting probability = 1/6
            bullet = {}
            bullet.x = self.enemies[i].x + ENEMY_WIDTH / 2 - BULLET_WIDTH / 2
            bullet.y = self.enemies[i].y
            table.insert(self.enemies[i].bullets, bullet)
            --end
        end
    end
    table.insert(self.enemies, enemy)
end

function detectCollisions(enemies, bullets)
    for i, enemy in ipairs(enemies) do
        for j, bullet in ipairs(bullets) do
            if bullet.y <= enemy.y + ENEMY_HEIGHT and bullet.x > enemy.x and bullet.x < enemy.x + ENEMY_WIDTH then
                table.remove(enemies, i)
                table.remove(player.bullets, j)
                love.audio.play(enemy_killed_sound)
            end
        end
    end
end

function love.update()
    if not game_won and not game_over then

        player.reload_time = player.reload_time - 1

        if love.keyboard.isDown("left") then
            player.x = player.x - PLAYER_SPEED
        elseif love.keyboard.isDown("right") then
            player.x = player.x + PLAYER_SPEED
        end

        if love.keyboard.isDown("space") then
            player.fire()
        end

        if #enemies_controller.enemies == 0 then
            game_won = true
        end

        for i, enemy in ipairs(enemies_controller.enemies) do
            enemy.reload_time = enemies_controller.enemies[i].reload_time - 1
            enemy.fire(i)
        end

        for i, enemy in ipairs(enemies_controller.enemies) do
            for j, bullet in ipairs(enemy.bullets) do
                if bullet.y < -10 then
                    table.remove(enemy.bullets, j)
                end
                bullet.y = bullet.y + 1
            end
        end

        for i, bullet in ipairs(player.bullets) do
            if bullet.y < -10 then
                table.remove(player.bullets, i)
            end
            bullet.y = bullet.y - 10
        end

        for _, enemy in pairs(enemies_controller.enemies) do
            if enemy.y >= love.graphics.getHeight() then
                game_over = true
            end
            enemy.y = enemy.y + ENEMY_SPEED
            enemy.x = enemy.x + math.sin(love.timer.getTime()) / 2
        end

        detectCollisions(enemies_controller.enemies, player.bullets)
    end
end

function love.draw()
    --love.graphics.print("Hello World!", 100, 100)

    if game_over then
        love.graphics.print("GAME OVER!!!", love.graphics.getWidth() / 2 - 40, love.graphics.getHeight() / 2 - 10)
        return
    elseif game_won then
        love.graphics.print("YOU WON!!!", love.graphics.getWidth() / 2 - 40, love.graphics.getHeight() / 2 - 10)
        return
    end

    love.graphics.draw(background_image)
    love.graphics.draw(player.image, player.x, player.y)

    for _, enemy in pairs(enemies_controller.enemies) do
        love.graphics.draw(enemies_controller.image, enemy.x, enemy.y)
    end

    for _, bullet in pairs(player.bullets) do
        --love.graphics.rectangle("fill", bullet.x, bullet.y, BULLET_WIDTH, BULLET_HEIGHT)
        love.graphics.draw(bullet_image, bullet.x, bullet.y)
    end

    for _, enemy in pairs(enemies_controller.enemies) do
        for _, bullet in pairs(enemy.bullets) do
            love.graphics.draw(bullet_image, bullet.x, bullet.y)
        end
    end
end