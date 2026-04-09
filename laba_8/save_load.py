def save_state(filename, balls, canvas_settings, screen_settings):

    try:
        save_data = {
            'balls': [],
            'canvas_settings': canvas_settings,
            'screen_settings': screen_settings
        }
        

        for ball in balls:
            ball_data = {
                'x': ball.x,
                'y': ball.y,
                'radius': ball.radius,
                'color': ball.color,
                'vx': ball.vx,
                'vy': ball.vy,
                'ay': ball.ay,
                'wind': ball.wind,
                'mass': ball.mass,
                'freezemode': ball.freezemode
            }
            save_data['balls'].append(ball_data)
        

        with open(filename, 'w') as f:
            print(save_data, file=f)
            pass
        
        return {
            'success': True,
            'message': f'Сохранено {len(balls)} шаров в файл {filename}',
            'filename': filename,
            'balls_count': len(balls)
        }
        
    except Exception as e:
        return {
            'success': False,
            'message': f'Ошибка при сохранении: {str(e)}',
            'error': str(e)
        }

def load_state(filename, create_ball_func, canvas, cw, ch):
    
    try:
        

        with open(filename, 'r') as f:
            load_data = f.read()
            load_data = eval(load_data)
        
        new_balls = []
        for ball_data in load_data['balls']:
            config = {
                'x': ball_data['x'],
                'y': ball_data['y'],
                'radius': ball_data['radius'],
                'color': ball_data['color'],
                'vx': ball_data['vx'],
                'vy': ball_data['vy'],
                'ay': ball_data['ay'],
                'wind': ball_data['wind'],
                'mass': ball_data['mass'],
                'freezemode': ball_data['freezemode']
            }
            
            radius = config['radius']
            if config['x'] + radius > cw:
                config['x'] = cw - radius
            if config['x'] - radius < 0:
                config['x'] = radius
            if config['y'] + radius > ch:
                config['y'] = ch - radius
            if config['y'] - radius < 0:
                config['y'] = radius
            
            new_ball = create_ball_func(config, canvas)
            new_balls.append(new_ball)
        
        return {
            'success': True,
            'message': f'Загружено {len(new_balls)} шаров из файла {filename}',
            'filename': filename,
            'balls': new_balls,
            'canvas_settings': load_data.get('canvas_settings', {}),
            'screen_settings': load_data.get('screen_settings', {})
        }
        
    except Exception as e:
        return {
            'success': False,
            'message': f'Ошибка при загрузке: {str(e)}',
            'error': str(e),
            'balls': [],
            'canvas_settings': None,
            'screen_settings': None
        }