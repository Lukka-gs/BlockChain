import hashlib 
import requests # type: ignore
import datetime as date

class Block:
    def __init__(self, index, timestamp, data, previous_hash):
        self.index = index  # Índice do bloco na blockchain
        self.timestamp = timestamp  # Data e hora em que o bloco foi criado
        self.data = data  # Dados armazenados no bloco
        self.previous_hash = previous_hash  # Hash do bloco anterior na cadeia
        self.hash = self.calculate_hash()  # Calcula o hash do bloco atual

    def calculate_hash(self):
        sha = hashlib.sha3_512()  # Cria um objeto sha3_512 (SHA-3_512 é uma função de hash criptográfica da família SHA-3, projetada pelo Instituto Nacional de Padrões e Tecnologia (NIST). Ela produz um valor de hash de 512 bits)
        sha.update(str(self.index).encode('utf-8') + # Atualiza o objeto sha com os dados do bloco convertidos para bytes
                   str(self.timestamp).encode('utf-8') +
                   str(self.data).encode('utf-8') +
                   str(self.previous_hash).encode('utf-8'))
        return sha.hexdigest()  # Retorna o hash calculado como uma string hexadecimal

class BlockChain:
    def __init__(self):
        # Inicializa a blockchain com o bloco gênese
        self.chain = [self.create_genesis_block()]

    def create_genesis_block(self):
        # Cria e retorna o bloco gênese, que é o primeiro bloco da cadeia
        return Block(0, date.datetime.now(), 'Genesis Block', '0')

    def add_block(self, new_block):
        # Adiciona o novo bloco à cadeia
        new_block.previous_hash = self.chain[-1].hash
        new_block.hash = new_block.calculate_hash()
        self.chain.append(new_block)

    def is_valid(self):
        # Verifica se a blockchain é válida percorrendo todos os blocos
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i - 1]

            if current_block.hash != current_block.calculate_hash():
                return False
            if current_block.previous_hash != previous_block.hash:
                return False
            
        return True

def get_crypto_price(symbol):
    try:
        url = f'https://api.coingecko.com/api/v3/simple/price?ids={symbol}&vs_currencies=usd' # URL da API CoinGecko para obter o preço da criptomoeda
        response = requests.get(url) # Faz uma solicitação GET para a API
        data = response.json() # Converte a resposta para JSON
        if symbol in data:
            return data[symbol]['usd'] # Retorna o preço da criptomoeda especificada em Dolares
        else:
            return None
    except Exception as e:
        print(f"Ocorreu um erro ao obter o preço da criptomoeda {symbol}: {e}")
        return None

def print_blockchain(chain):
    # Imprime todos os blocos na blockchain
    for block in chain:
        print(f'Block: {block.index}')
        print(f'Timestamp: {block.timestamp}')
        print(f'Data: {block.data}')
        print(f'Hash: {block.hash}')
        print(f'Previous Hash: {block.previous_hash}')
        print(20 * '-----')

def print_blockchain_data(chain):
    # Imprime apenas os dados dos blocos na blockchain
    for block in chain:
        print(f'Data do Bloco {block.index}: {block.data}')

def menu():
    while True:
        print("\nMenu:")
        print("1- Ver Blockchain (Data)")
        print("2- Ver Blockchain (Info completa)")
        print("3- Adicionar Block")
        print("4- Preço das Cryptos (Bitcoin, Ethereum, Solana, Near, Cardano, BNB, Cronos)")
        print("5- Verificar Validade da Blockchain")
        print("6- Sair")
        choice = input("Escolha uma opção: ")
        
        if choice == '1':
            print("Blockchain (Data):")
            print_blockchain_data(my_blockchain.chain)
        elif choice == '2':
            print("Blockchain (Info completa):")
            print_blockchain(my_blockchain.chain)
        elif choice == '3':
            item = input("Digite o nome do item: ")
            valor = input("Digite o valor do item em USD: ")
            comprador = input("Digite o nome do comprador: ")
            vendedor = input("Digite o nome do vendedor: ")
            data = {'Item': item, 'Valor':  f'US${valor}', 'Comprador': comprador, 'Vendedor': vendedor}
            my_blockchain.add_block(Block(len(my_blockchain.chain), date.datetime.now(), data, my_blockchain.chain[-1].hash))
            print("Bloco adicionado com sucesso!")
        elif choice == '4':
            bitcoin_price = get_crypto_price("bitcoin")
            ethereum_price = get_crypto_price("ethereum")
            solana_price = get_crypto_price("solana")
            near_price = get_crypto_price("near")
            bnb_price = get_crypto_price("bnb")
            
            if bitcoin_price is not None:
                print(f'Bitcoin: US${bitcoin_price:.2f}')
            else:
                print("O preço da criptomoeda Bitcoin não pôde ser obtido no momento.")
                
            if ethereum_price is not None:
                print(f'Ethereum: US${ethereum_price:.2f}')
            else:
                print("O preço da criptomoeda Ethereum não pôde ser obtido no momento.")
                
            if solana_price is not None:
                print(f'Solana: US${solana_price:.2f}')
            else:
                print("O preço da criptomoeda Solana não pôde ser obtido no momento.")
                
            if near_price is not None:
                print(f'Near: US${near_price:.2f}')
            else:
                print("O preço da criptomoeda Near não pôde ser obtido no momento.")
                
            if bnb_price is not None:
                print(f'Binance Coin: US${bnb_price:.2f}')
            else:
                print("O preço da criptomoeda Binance Coin não pôde ser obtido no momento.")
        elif choice == '5':
            print(f'Essa Blockchain está válida? {str(my_blockchain.is_valid())}')
        elif choice == '6':
            print("Saindo...")
            break
        else:
            print("Opção inválida!")

# Criação da blockchain
my_blockchain = BlockChain()

if __name__ == "__main__":
    menu()
