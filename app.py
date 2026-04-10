from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = 'gorjeta_trp1_secret_key_trp1'


@app.route('/', methods=['Get', 'POST'])
def index():
    return render_template('index.html')


@app.route('/formulario')
def formulario():
    return render_template('formulario.html')


# Rota que processa o cálculo e exibe o resultado
@app.route('/calcular', methods=['GET', 'POST'])
def calcular(): # Este nome aqui é o que o url_for('calcular') busca

    # Se o usuário apenas "entrou" na página (pelo menu ou link)
    if request.method == 'GET':
        return redirect(url_for('formulario'))

    # 1. Coleta os valores do formulário
    distancia_conta = request.form.get('distancia_conta')
    consumo_conta = request.form.get('consumo_conta')
    preco_conta = request.form.get('preco_conta')


    # 2. Validação: Verifica se os campos estão preenchidos usando 'if not'
    if not distancia_conta:
        flash(f"O campo 'Distância' é obrigatório!", 'danger')
        return render_template('formulario.html')
    
    if not consumo_conta:
        flash(f"O campo 'Consumo' é obrigatório!", 'danger')
        return render_template('formulario.html')
    
    if not preco_conta:
        flash(f"O campo 'Preço' é obrigatório!", 'danger')
        return render_template('formulario.html')
    
    distancia_conta = float(distancia_conta)
    consumo_conta = float(consumo_conta)
    preco_conta = float(preco_conta)


    # 4. Validações de Regra de Negócio
    if distancia_conta <= 0:
        flash(f'A distância deve ser maior que zero.', 'danger')
        return render_template('formulario.html')
       
    elif consumo_conta <= 0:
        flash(f'O consumo deve ser maior que 0.', 'danger')
        return render_template('formulario.html')

    elif preco_conta < 0:
        flash(f'O preço deve ser maior que zero.', 'danger')
        return render_template('formulario.html')
    

    # 5. Cálculos
    litros_necessarios = distancia_conta / consumo_conta
    custo_total_viagem = round(litros_necessarios * preco_conta)
    custo_por_km_rodado = custo_total_viagem / distancia_conta
   

    # 6. Determinar Classificação
    if consumo_conta == 8:
        classificacao = 'Padrão'
    elif consumo_conta == 15:
        classificacao = 'Padrão'
    elif consumo_conta == 18:
        classificacao = 'Econômico'
    elif consumo_conta > 15 and consumo_conta < 18:
        classificacao = 'Econômico'
    elif consumo_conta < 8:
        classificacao = 'Beberrão'
    elif consumo_conta > 8 and consumo_conta < 15:
        classificacao = 'Padrão'
    else:
        classificacao = 'Super Econômico'
   

    # 7. Exibição dos resultados
    dados_para_tabela = [{
            'distancia_conta': distancia_conta,
            'consumo_conta': consumo_conta,
            'preco_conta': preco_conta,
            'litros_necessarios': litros_necessarios,
            'custo_total_viagem': custo_total_viagem,
            'custo_por_km_rodado': custo_por_km_rodado,
            'classificacao': classificacao
    }]
    
    return render_template('resultados.html', calculos=dados_para_tabela, total=1)


if __name__ == '__main__':
    app.run(debug=True)



"""
No Flask, o url_for('nome') procura o nome da função dentro do Python,
e não o nome do arquivo .html.
"""