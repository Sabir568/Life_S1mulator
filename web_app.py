<!DOCTYPE html>
<html lang="uk">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Точка Доступних Цін</title>
    <style>
        /* Umumiy ko'rinish */
        body {
            font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
            margin: 0;
            padding: 0;
            background-color: #f8f9fa;
            color: #333;
        }

        /* Ukraina uslubidagi Header */
        header {
            background: linear-gradient(135deg, #0057b7 0%, #0057b7 50%, #ffd700 50%, #ffd700 100%);
            color: white;
            padding: 60px 20px;
            text-align: center;
            box-shadow: 0 4px 15px rgba(0,0,0,0.2);
        }

        header h1 {
            margin: 0;
            font-size: 3rem;
            text-shadow: 2px 2px 8px rgba(0,0,0,0.4);
            letter-spacing: 2px;
        }

        header p {
            font-size: 1.2rem;
            margin-top: 10px;
            background: rgba(0,0,0,0.3);
            display: inline-block;
            padding: 5px 15px;
            border-radius: 20px;
        }

        /* Katalog qismi */
        .container {
            max-width: 1200px;
            margin: 40px auto;
            padding: 20px;
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 30px;
        }

        /* Mahsulot kartalari */
        .card {
            background: white;
            border-radius: 20px;
            overflow: hidden;
            box-shadow: 0 10px 20px rgba(0,0,0,0.05);
            transition: all 0.3s ease;
            border: 1px solid #eee;
            text-align: center;
            padding-bottom: 20px;
        }

        .card:hover {
            transform: translateY(-10px);
            box-shadow: 0 15px 30px rgba(0,0,0,0.1);
            border-color: #0057b7;
        }

        .icon-box {
            height: 180px;
            background-color: #f1f4f8;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 80px;
        }

        .card h2 {
            margin: 20px 0 10px;
            color: #0057b7;
        }

        .card p {
            color: #888;
            font-size: 0.9rem;
            padding: 0 15px;
        }

        .status-badge {
            background-color: #ff4757;
            color: white;
            padding: 5px 12px;
            border-radius: 15px;
            font-size: 0.8rem;
            display: inline-block;
            margin-top: 10px;
        }

        /* Footer */
        footer {
            background-color: #222;
            color: #777;
            text-align: center;
            padding: 40px 20px;
            margin-top: 60px;
        }

        .contact-info {
            color: #ffd700;
            margin-bottom: 10px;
        }
    </style>
</head>
<body>

<header>
    <h1>Точка Доступних Цін</h1>
    <p>Ласкаво просимо до нашого онлайн-магазину!</p>
</header>

<div class="container">
    <div class="card">
        <div class="icon-box">👟</div>
        <h2>Взуття</h2>
        <p>Великий вибір чоловічого та жіночого взуття.</p>
        <div class="status-badge">Фото з'являться незабаром</div>
    </div>

    <div class="card">
        <div class="icon-box">👕</div>
        <h2>Одяг</h2>
        <p>Стильний та комфортний одяг на кожен день.</p>
        <div class="status-badge">Фото з'являться незабаром</div>
    </div>

    <div class="card">
        <div class="icon-box">🩱</div>
        <h2>Білизна</h2>
        <p>Якісна білизна за найкращими цінами.</p>
        <div class="status-badge">Фото з'являться незабаром</div>
    </div>

    <div class="card">
        <div class="icon-box">👜</div>
        <h2>Сумки</h2>
        <p>Аксесуари, що доповнять ваш образ.</p>
        <div class="status-badge">Фото з'являться незабаром</div>
    </div>
</div>

<footer>
    <div class="contact-info">Скоро відкриття асортименту!</div>
    <p>&copy; 2026 Точка Доступних Цін. Україна.</p>
</footer>

</body>
</html>
