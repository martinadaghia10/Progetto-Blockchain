import matplotlib.pyplot as plt
import pandas as pd

# Specifica i tipi di dati per le colonne 6 e 9
dtype_dict = {'token_id': 'str', 'currency_address': 'str'}

# Carica i dati degli scambi NFT con i tipi di dati specificati
nft_trades_df = pd.read_csv('./database/nfts/nft_trades.csv', dtype=dtype_dict)
merged_twitter_data_df = pd.read_csv('./merged_twitter_data.csv')

print("Colonne disponibili in nft_trades_df:")
print(nft_trades_df.columns)

# Estrai l'anno dalla colonna 'date'
nft_trades_df['year'] = pd.to_datetime(nft_trades_df['date']).dt.year

# Scoprire gli anni più importanti dai plot
for feature in ["avg_price", "usd_amount"]:
    plt.figure(figsize=(10, 6))

    for year in nft_trades_df['year'].unique():
        year_data = nft_trades_df[nft_trades_df['year'] == year]
        plt.plot(year_data['date'], year_data[feature], label=str(year))

    # Riduci il numero di punti visualizzati campionando casualmente i dati
    sample_size = 1000  # Scegli il numero di punti da visualizzare
    sampled_data = nft_trades_df.sample(n=sample_size, random_state=42)

    # Visualizza il grafico
    plt.plot(sampled_data['date'], sampled_data[feature], label=f"Sampled Data ({sample_size} points)")
    plt.title(f"{feature} per anno")
    plt.xlabel('Data')
    plt.ylabel(feature)
    plt.legend(loc='upper left')
    plt.show()

'''
# scoprire gli anni più importanti dai plot
for feature in ["avg_price", "usd_amount"]:
    plt.figure(figsize=(10, 6))
    for year in nft_trades_df['year'].unique():
        year_data = nft_trades_df[dataframe['year'] == year]
        plt.plot(year_data['date'], year_data[feature], label=str(year))

    plt.title(f"{feature} per anno")
    plt.xlabel('Data')
    plt.ylabel(feature)
    plt.legend(loc='upper left')
    plt.show()


'''
def find_peaks(data, threshold):
    # Converti la colonna 'date' nel formato datetime
    data['date'] = pd.to_datetime(data['date'])
    # Estrai l'anno dalla colonna 'date'
    data['year'] = data['date'].dt.year
    # Filtra i dati per gli anni 2021 e 2022
    data_2021_2022 = data[data['year'].isin([2021, 2022])]
    # Trova i picchi che superano la soglia
    peaks = data_2021_2022[data_2021_2022['avg_price'] > threshold]
    # Stampa i picchi che superano la soglia, ordinati per data, mostrando solo alcune colonne
    '''
    print("Picchi che superano la soglia:")
    print(peaks.sort_values(by='date')[
              ['date', 'avg_price', 'contract_address', 'transaction_hash', 'num_items', 'seller', 'buyer', 'token_id',
               'currency', 'currency_address', 'usd_amount', 'platform']])
    # Disegna un grafico per visualizzare i picchi
    plt.figure(figsize=(10, 6))
    plt.plot(data_2021_2022['date'], data_2021_2022['avg_price'], label='avg_price')
    plt.scatter(peaks['date'], peaks['avg_price'], color='red', label='Picchi')
    plt.xlabel('Data')
    plt.ylabel('avg_price')
    plt.title('Individuazione dei picchi di avg_price')
    plt.legend()
    plt.show()
    '''
    return peaks


# Chiama la funzione find_peaks con il DataFrame e la soglia desiderata
peaks = find_peaks(nft_trades_df, threshold=80000)
def find_tweets_before_peaks(twitter_data, peaks, days_before):
    # Converti le colonne 'created_at' nel formato datetime
    twitter_data['created_at'] = pd.to_datetime(twitter_data['created_at'])
    peaks['date'] = pd.to_datetime(peaks['date'])
    # Estrai le date dei picchi
    peak_dates = peaks['date']
    tweets_before_peaks_list = []

    # Itera attraverso i picchi
    for i, peak_date in enumerate(peak_dates):
        # Trova tutti i tweet nei giorni precedenti al picco corrente
        tweets_before_peak = twitter_data[
            twitter_data['created_at'].between(peak_date - pd.Timedelta(days=days_before), peak_date)]
        # Rimuovi i duplicati
        tweets_before_peak = tweets_before_peak.drop_duplicates(subset=['created_at', 'user_id', 'tweet_id'])
        # Rimuovi i valori nulli
        tweets_before_peak = tweets_before_peak.dropna()
        # Aggiungi i risultati alla lista
        tweets_before_peaks_list.append(tweets_before_peak)
        # Stampa i risultati
        '''
        print(f"Tweet fatti massimo {days_before} giorni prima del PICCO {i + 1} ({peaks.iloc[i]['date']}):")
        print(tweets_before_peak)
        print("\n" + "-" * 50 + "\n")
        '''
    return tweets_before_peaks_list


# Trova i tweet fatti massimo 2 giorni prima di ciascun picco ottenuto in precedenza
tweets_before_peaks_list = find_tweets_before_peaks(merged_twitter_data_df, peaks, days_before=2)
# questo è il 5% dei tweet più influenti
retweet_percentile = tweets_before_peaks_list[0]['retweet_count'].quantile(0.95)  # Ad esempio, il 95° percentile
like_percentile = tweets_before_peaks_list[0]['like_count'].quantile(0.95)  # Ad esempio, il 95° percentile
'''
print(f"retweet_condition calcolato come {retweet_percentile}")
print(f"like_condition calcolato come {like_percentile}")
'''
def influential_tweets(like, retweet):
    # Filtra i tweet con retweet_count maggiore di 200
    filtered_tweets_list = [tweets[(tweets['retweet_count'] > retweet) & (tweets['like_count'] > like)]
                            for tweets in tweets_before_peaks_list]
    '''
    # Stampa i risultati
    for i, filtered_tweets in enumerate(filtered_tweets_list):
        print(f"Tweet con retweet_count > {retweet} e like_count > {like} --> massimo 2 giorni prima del picco 
        numero {i+1} ({peaks.iloc[i]['date']}):")
        print(filtered_tweets)
        print("\n" + "-"*200 + "\n")
    '''
    return filtered_tweets_list


filtered_tweets_list = influential_tweets(like_percentile, retweet_percentile)

# Crea una lista di set di user_id per ciascun picco
user_id_sets = [set(tweets_before_peak['user_id']) for tweets_before_peak in tweets_before_peaks_list]

# Trova l'intersezione degli insiemi
common_user_ids = set.intersection(*user_id_sets)

# Stampa gli user_id comuni a tutti i 9 picchi
print("Gli user_id comuni a tutti i 9 picchi sono:")
print(common_user_ids)

common_user_tweets = merged_twitter_data_df[merged_twitter_data_df['user_id'].isin(common_user_ids)]
'''
# Stampa il numero di retweet e like per gli user_id comuni
print("Numero di retweet e like per gli user_id comuni:")
print(common_user_tweets.groupby('user_id')[['retweet_count', 'like_count']].sum())
'''
# Calcola la somma di retweet e like per ciascun user_id
user_totals = common_user_tweets.groupby('user_id').agg({'retweet_count': 'sum', 'like_count': 'sum', 'hashtag': 'sum',
                                                         'collection': 'sum'})

# Calcola i percentili basati sulla somma di retweet e like
retweet_percentile_common_user = user_totals['retweet_count'].quantile(0.75)
like_percentile_common_user = user_totals['like_count'].quantile(0.75)
'''
# Stampa i risultati
print(f"retweet comuni a tutti i picchi e più influenti --> {retweet_percentile_common_user}")
print(f"like comuni a tutti i picchi e più influenti --> {like_percentile_common_user}")
'''
# Filtra gli user_id che superano le soglie
influential_users = user_totals[(user_totals['retweet_count'] > retweet_percentile_common_user)
                                & (user_totals['like_count'] > like_percentile_common_user)]

# Stampa gli user_id influenti
print("Gli user_id influenti che superano le soglie del 25%:")
influential_users=influential_users[['retweet_count', 'like_count']]
print(influential_users)

influential_users_data = merged_twitter_data_df[merged_twitter_data_df['user_id'].isin(influential_users.index)]

#da qui non so come andare avanti, bisogna arrivare ad una soluzione insieme

