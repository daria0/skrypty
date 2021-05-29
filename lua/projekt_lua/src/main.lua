---
--- Created by Daria Siemieniuk
--- project: SPACE INVADERS USING LUA & LOVE
---


--- CONFIG:
RELOAD_TIME = 15
BASE_POINTS_FOR_KILLING = 10
--- PLAYER
PLAYER_WIDTH = 22
PLAYER_HEIGHT = 22
PLAYER_X = (love.graphics.getWidth() - PLAYER_WIDTH) / 2
PLAYER_Y = 570
PLAYER_SPEED = 5
--- BULLET
BULLET_WIDTH = 4
BULLET_HEIGHT = 8
PLAYER_BULLET_SPEED = 8
ENEMY_BULLET_SPEED = 2
--- ENEMY
ENEMY_X = 0
ENEMY_Y = 0
ENEMY_WIDTH = 28
ENEMY_HEIGHT = 20
ENEMY_SPEED = 0.2
SPACE_BETWEEN_ENEMIES = 50
NUMBER_OF_ENEMIES = 20
NUMBER_OF_ROWS = 5
NUMBER_OF_ENEMIES_IN_ONE_ROW = NUMBER_OF_ENEMIES / NUMBER_OF_ROWS

--in case of changing scale of the images:
love.graphics.setDefaultFilter("nearest", "nearest")

enemy = {}
enemies_controller = {}
enemies_controller.enemies = {}
enemies_controller.image = {}
enemies_controller.image[1] = love.graphics.newImage("enemy1.png")
enemies_controller.image[2] = love.graphics.newImage("enemy2.png")
enemies_controller.image[3] = love.graphics.newImage("enemy3.png")
enemies_controller.image[4] = love.graphics.newImage("enemy4.png")
enemies_controller.image[5] = love.graphics.newImage("enemy5.png")
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
    player.score = 0
    player.bullets = {}
    player.reload_time = RELOAD_TIME
    player.fire_sound = love.audio.newSource("shoot.wav", "static")
    player.explosion_sound = love.audio.newSource("explosion.wav", "static")
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

    enemies_width = NUMBER_OF_ENEMIES_IN_ONE_ROW * (ENEMY_WIDTH + SPACE_BETWEEN_ENEMIES) - SPACE_BETWEEN_ENEMIES
    for i = 1, NUMBER_OF_ROWS do
        for j = 1, NUMBER_OF_ENEMIES_IN_ONE_ROW do
            enemies_controller:spawnEnemy(love.graphics.getWidth() / 2 - enemies_width / 2 + (j - 0.5) * SPACE_BETWEEN_ENEMIES, i * SPACE_BETWEEN_ENEMIES, (i - 1) * NUMBER_OF_ENEMIES_IN_ONE_ROW + j, NUMBER_OF_ROWS - i + 1)
        end
    end

    for i, enemy in ipairs(enemies_controller.enemies) do
        if i > (NUMBER_OF_ENEMIES - NUMBER_OF_ENEMIES_IN_ONE_ROW) then
            enemy.free_to_shoot = true
        end
    end
end

function enemies_controller:spawnEnemy(x, y, index, level)
    enemy = {}
    enemy.x = x
    enemy.y = y
    enemy.index = index
    enemy.level = level
    enemy.bullets = {}
    enemy.reload_time = (6 - level) * RELOAD_TIME
    enemy.free_to_shoot = false
    enemy.fire = function(i)
        if self.enemies[i].reload_time <= 0 and self.enemies[i].free_to_shoot then
            self.enemies[i].reload_time = 5 * RELOAD_TIME
            if math.random(0, 1) == 1 then
                --shooting probability = 1/2
                bullet = {}
                bullet.x = self.enemies[i].x + ENEMY_WIDTH / 2 - BULLET_WIDTH / 2
                bullet.y = self.enemies[i].y
                table.insert(self.enemies[i].bullets, bullet)
            end
        end
    end
    table.insert(self.enemies, enemy)
end

function has_value (tab, val)
    for _, value in ipairs(tab) do
        if value == val then
            return true
        end
    end
    return false
end

function clearToShoot(i)
    column_counter = 0
    indexes_to_check = {}
    for j = (i - NUMBER_OF_ENEMIES_IN_ONE_ROW), NUMBER_OF_ENEMIES, NUMBER_OF_ENEMIES_IN_ONE_ROW do
        table.insert(indexes_to_check, j)
    end
    for _, enemy in pairs(enemies_controller.enemies) do
        if has_value(indexes_to_check, enemy.index) then
            column_counter = column_counter + 1
        end
    end

    if column_counter == 1 then
        for _, enemy in pairs(enemies_controller.enemies) do
            if enemy.index == i - NUMBER_OF_ENEMIES_IN_ONE_ROW then
                enemy.free_to_shoot = true
            end
        end
    end
end

function detectCollisions(enemies, bullets)
    for i, enemy in ipairs(enemies) do
        for j, bullet in ipairs(bullets) do
            if bullet.y <= enemy.y + ENEMY_HEIGHT and bullet.x > enemy.x and bullet.x < enemy.x + ENEMY_WIDTH then
                index = enemy.index
                table.remove(enemies, i)
                table.remove(player.bullets, j)
                -- now enable enemy with index: enemy.i - NUMBER_OF_ENEMIES_IN_ONE_ROW to shoot
                clearToShoot(enemy.index)
                player.score = player.score + BASE_POINTS_FOR_KILLING * enemy.level
                love.audio.play(enemy_killed_sound)
            end
        end
    end
end

function detectPlayerKilled(enemies)
    for _, enemy in pairs(enemies) do
        for _, bullet in pairs(enemy.bullets) do
            if bullet.y >= player.y and bullet.x > player.x and bullet.x < player.x + PLAYER_WIDTH then
                love.audio.play(player.explosion_sound)
                game_over = true
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

        for _, enemy in pairs(enemies_controller.enemies) do
            for j, bullet in ipairs(enemy.bullets) do
                if bullet.y > love.graphics.getHeight() then
                    table.remove(enemy.bullets, j)
                end
                bullet.y = bullet.y + ENEMY_BULLET_SPEED
            end
        end

        for i, bullet in ipairs(player.bullets) do
            if bullet.y < -10 then
                table.remove(player.bullets, i)
            end
            bullet.y = bullet.y - PLAYER_BULLET_SPEED
        end

        for _, enemy in pairs(enemies_controller.enemies) do
            if enemy.y >= love.graphics.getHeight() then
                game_over = true
            end
            enemy.y = enemy.y + ENEMY_SPEED
            enemy.x = enemy.x + math.sin(love.timer.getTime()) / 2
        end

        detectCollisions(enemies_controller.enemies, player.bullets)
        detectPlayerKilled(enemies_controller.enemies)
    end
end

function love.draw()

    if game_over then
        love.graphics.print("GAME OVER!!!", love.graphics.getWidth() / 2 - 40, love.graphics.getHeight() / 2 - 10)
        return
    elseif game_won then
        love.graphics.print("YOU WON!!!", love.graphics.getWidth() / 2 - 40, love.graphics.getHeight() / 2 - 10)
        return
    end

    love.graphics.draw(background_image)
    love.graphics.print("SCORE:", 10, 10)
    love.graphics.print(player.score, 70, 10)
    love.graphics.draw(player.image, player.x, player.y)

    for _, enemy in pairs(enemies_controller.enemies) do
        love.graphics.draw(enemies_controller.image[enemy.level], enemy.x, enemy.y)
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