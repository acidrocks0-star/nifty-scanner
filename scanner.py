import yfinance as yf
import pandas as pd
import numpy as np
from ta.trend import ADXIndicator
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

# CLEANED NIFTY 500 LIST - Apr 2026
nifty500 = [
'360ONE.NS', '3MINDIA.NS', 'ABB.NS', 'ACC.NS', 'ACMESOLAR.NS', 'AIAENG.NS', 'APLAPOLLO.NS', 'AUBANK.NS', 'AWL.NS', 'AADHARHFC.NS', 'AARTIIND.NS', 'AAVAS.NS', 'ABBOTINDIA.NS', 'ACE.NS', 'ACUTAAS.NS', 'ADANIENSOL.NS', 'ADANIENT.NS', 'ADANIGREEN.NS', 'ADANIPORTS.NS', 'ADANIPOWER.NS', 'ATGL.NS', 'ABCAPITAL.NS', 'ABFRL.NS', 'ABLBL.NS', 'ABREL.NS', 'ABSLAMC.NS', 'CPPLUS.NS', 'AEGISLOG.NS', 'AEGISVOPAK.NS', 'AFCONS.NS', 'AFFLE.NS', 'AJANTPHARM.NS', 'ALKEM.NS', 'ABDL.NS', 'ARE&M.NS', 'AMBER.NS', 'AMBUJACEM.NS', 'ANANDRATHI.NS', 'ANANTRAJ.NS', 'ANGELONE.NS', 'ANTHEM.NS', 'ANURAS.NS', 'APARINDS.NS', 'APOLLOHOSP.NS', 'APOLLOTYRE.NS', 'APTUS.NS', 'ASAHIINDIA.NS', 'ASHOKLEY.NS', 'ASIANPAINT.NS', 'ASTERDM.NS', 'ASTRAL.NS', 'ATHERENERG.NS', 'ATUL.NS', 'AUROPHARMA.NS', 'AIIL.NS', 'DMART.NS', 'AXISBANK.NS', 'BEML.NS', 'BLS.NS', 'BSE.NS', 'BAJAJ-AUTO.NS', 'BAJFINANCE.NS', 'BAJAJFINSV.NS', 'BAJAJHLDNG.NS', 'BAJAJHFL.NS', 'BALKRISIND.NS', 'BALRAMCHIN.NS', 'BANDHANBNK.NS', 'BANKBARODA.NS', 'BANKINDIA.NS', 'MAHABANK.NS', 'BATAINDIA.NS', 'BAYERCROP.NS', 'BELRISE.NS', 'BERGEPAINT.NS', 'BDL.NS', 'BEL.NS', 'BHARATFORG.NS', 'BHEL.NS', 'BPCL.NS', 'BHARTIARTL.NS', 'BHARTIHEXA.NS', 'BIKAJI.NS', 'GROWW.NS', 'BIOCON.NS', 'BSOFT.NS', 'BLUEDART.NS', 'BLUEJET.NS', 'BLUESTARCO.NS', 'BBTC.NS', 'BOSCHLTD.NS', 'FIRSTCRY.NS', 'BRIGADE.NS', 'BRITANNIA.NS', 'MAPMYINDIA.NS', 'CCL.NS', 'CESC.NS', 'CGPOWER.NS', 'CRISIL.NS', 'CANFINHOME.NS', 'CANBK.NS', 'CANHLIFE.NS', 'CAPLIPOINT.NS', 'CGCL.NS', 'CARBORUNIV.NS', 'CARTRADE.NS', 'CASTROLIND.NS', 'CEATLTD.NS', 'CEMPRO.NS', 'CENTRALBK.NS', 'CDSL.NS', 'CHALET.NS', 'CHAMBLFERT.NS', 'CHENNPETRO.NS', 'CHOICEIN.NS', 'CHOLAHLDNG.NS', 'CHOLAFIN.NS', 'CIPLA.NS', 'CUB.NS', 'CLEAN.NS', 'COALINDIA.NS', 'COCHINSHIP.NS', 'COFORGE.NS', 'COHANCE.NS', 'COLPAL.NS', 'CAMS.NS', 'CONCORDBIO.NS', 'CONCOR.NS', 'COROMANDEL.NS', 'CRAFTSMAN.NS', 'CREDITACC.NS', 'CROMPTON.NS', 'CUMMINSIND.NS', 'CYIENT.NS', 'DCMSHRIRAM.NS', 'DLF.NS', 'DOMS.NS', 'DABUR.NS', 'DALBHARAT.NS', 'DATAPATTNS.NS', 'DEEPAKFERT.NS', 'DEEPAKNTR.NS', 'DELHIVERY.NS', 'DEVYANI.NS', 'DIVISLAB.NS', 'DIXON.NS', 'LALPATHLAB.NS', 'DRREDDY.NS', 'EIDPARRY.NS', 'EIHOTEL.NS', 'EICHERMOT.NS', 'ELECON.NS', 'ELGIEQUIP.NS', 'EMAMILTD.NS', 'EMCURE.NS', 'EMMVEE.NS', 'ENDURANCE.NS', 'ENGINERSIN.NS', 'ERIS.NS', 'ESCORTS.NS', 'ETERNAL.NS', 'EXIDEIND.NS', 'NYKAA.NS', 'FEDERALBNK.NS', 'FACT.NS', 'FINCABLES.NS', 'FSL.NS', 'FIVESTAR.NS', 'FORCEMOT.NS', 'FORTIS.NS', 'GAIL.NS', 'GVT&D.NS', 'GMRAIRPORT.NS', 'GABRIEL.NS', 'GALLANTT.NS', 'GRSE.NS', 'GICRE.NS', 'GILLETTE.NS', 'GLAND.NS', 'GLAXO.NS', 'GLENMARK.NS', 'MEDANTA.NS', 'GODIGIT.NS', 'GPIL.NS', 'GODFRYPHLP.NS', 'GODREJCP.NS', 'GODREJIND.NS', 'GODREJPROP.NS', 'GRANULES.NS', 'GRAPHITE.NS', 'GRASIM.NS', 'GRAVITA.NS', 'GESHIP.NS', 'FLUOROCHEM.NS', 'GMDCLTD.NS', 'GSPL.NS', 'HEG.NS', 'HBLENGINE.NS', 'HCLTECH.NS', 'HDBFS.NS', 'HDFCAMC.NS', 'HDFCBANK.NS', 'HDFCLIFE.NS', 'HFCL.NS', 'HAVELLS.NS', 'HEROMOTOCO.NS', 'HEXT.NS', 'HSCL.NS', 'HINDALCO.NS', 'HAL.NS', 'HINDCOPPER.NS', 'HINDPETRO.NS', 'HINDUNILVR.NS', 'HINDZINC.NS', 'POWERINDIA.NS', 'HOMEFIRST.NS', 'HONASA.NS', 'HONAUT.NS', 'HUDCO.NS', 'HYUNDAI.NS', 'ICICIBANK.NS', 'ICICIGI.NS', 'ICICIAMC.NS', 'ICICIPRULI.NS', 'IDBI.NS', 'IDFCFIRSTB.NS', 'IFCI.NS', 'IIFL.NS', 'IRB.NS', 'IRCON.NS', 'ITCHOTELS.NS', 'ITC.NS', 'ITI.NS', 'INDGN.NS', 'INDIACEM.NS', 'INDIAMART.NS', 'INDIANB.NS', 'IEX.NS', 'INDHOTEL.NS', 'IOC.NS', 'IOB.NS', 'IRCTC.NS', 'IRFC.NS', 'IREDA.NS', 'IGL.NS', 'INDUSTOWER.NS', 'INDUSINDBK.NS', 'NAUKRI.NS', 'INFY.NS', 'INOXWIND.NS', 'INTELLECT.NS', 'INDIGO.NS', 'IGIL.NS', 'IKS.NS', 'IPCALAB.NS', 'JBCHEPHARM.NS', 'JKCEMENT.NS', 'JBMA.NS', 'JKTYRE.NS', 'JMFINANCIL.NS', 'JSWCEMENT.NS', 'JSWDULUX.NS', 'JSWENERGY.NS', 'JSWINFRA.NS', 'JSWSTEEL.NS', 'JAINREC.NS', 'JPPOWER.NS', 'J&KBANK.NS', 'JINDALSAW.NS', 'JSL.NS', 'JINDALSTEL.NS', 'JIOFIN.NS', 'JUBLFOOD.NS', 'JUBLINGREA.NS', 'JUBLPHARMA.NS', 'JWL.NS', 'JYOTICNC.NS', 'KPRMILL.NS', 'KEI.NS', 'KPITTECH.NS', 'KAJARIACER.NS', 'KPIL.NS', 'KALYANKJIL.NS', 'KARURVYSYA.NS', 'KAYNES.NS', 'KEC.NS', 'KFINTECH.NS', 'KIRLOSENG.NS', 'KOTAKBANK.NS', 'KIMS.NS', 'LTF.NS', 'LTTS.NS', 'LGEINDIA.NS', 'LICHSGFIN.NS', 'LTFOODS.NS', 'LTM.NS', 'LT.NS', 'LATENTVIEW.NS', 'LAURUSLABS.NS', 'THELEELA.NS', 'LEMONTREE.NS', 'LENSKART.NS', 'LICI.NS', 'LINDEINDIA.NS', 'LLOYDSME.NS', 'LODHA.NS', 'LUPIN.NS', 'MMTC.NS', 'MRF.NS', 'MGL.NS', 'M&MFIN.NS', 'M&M.NS', 'MANAPPURAM.NS', 'MRPL.NS', 'MANKIND.NS', 'MARICO.NS', 'MARUTI.NS', 'MFSL.NS', 'MAXHEALTH.NS', 'MAZDOCK.NS', 'MEESHO.NS', 'MINDACORP.NS', 'MSUMI.NS', 'MOTILALOFS.NS', 'MPHASIS.NS', 'MCX.NS', 'MUTHOOTFIN.NS', 'NATCOPHARM.NS', 'NBCC.NS', 'NCC.NS', 'NHPC.NS', 'NLCINDIA.NS', 'NMDC.NS', 'NSLNISP.NS', 'NTPCGREEN.NS', 'NTPC.NS', 'NH.NS', 'NATIONALUM.NS', 'NAVA.NS', 'NAVINFLUOR.NS', 'NESTLEIND.NS', 'NETWEB.NS', 'NEULANDLAB.NS', 'NEWGEN.NS', 'NAM-INDIA.NS', 'NIVABUPA.NS', 'NUVAMA.NS', 'NUVOCO.NS', 'OBEROIRLTY.NS', 'ONGC.NS', 'OIL.NS', 'OLAELEC.NS', 'OLECTRA.NS', 'PAYTM.NS', 'ONESOURCE.NS', 'OFSS.NS', 'POLICYBZR.NS', 'PCBL.NS', 'PGEL.NS', 'PIIND.NS', 'PNBHOUSING.NS', 'PTCIL.NS', 'PVRINOX.NS', 'PAGEIND.NS', 'PARADEEP.NS', 'PATANJALI.NS', 'PERSISTENT.NS', 'PETRONET.NS', 'PFIZER.NS', 'PHOENIXLTD.NS', 'PWL.NS', 'PIDILITIND.NS', 'PINELABS.NS', 'PIRAMALFIN.NS', 'PPLPHARMA.NS', 'POLYMED.NS', 'POLYCAB.NS', 'POONAWALLA.NS', 'PFC.NS', 'POWERGRID.NS', 'PREMIERENE.NS', 'PRESTIGE.NS', 'PNB.NS', 'RRKABEL.NS', 'RBLBANK.NS', 'RECLTD.NS', 'RHIM.NS', 'RITES.NS', 'RADICO.NS', 'RVNL.NS', 'RAILTEL.NS', 'RAINBOW.NS', 'RKFORGE.NS', 'REDINGTON.NS', 'RELIANCE.NS', 'RPOWER.NS', 'SBFC.NS', 'SBICARD.NS', 'SBILIFE.NS', 'SJVN.NS', 'SRF.NS', 'SAGILITY.NS', 'SAILIFE.NS', 'SAMMAANCAP.NS', 'MOTHERSON.NS', 'SAPPHIRE.NS', 'SARDAEN.NS', 'SAREGAMA.NS', 'SCHAEFFLER.NS', 'SCHNEIDER.NS', 'SCI.NS', 'SHREECEM.NS', 'SHRIRAMFIN.NS', 'SHYAMMETL.NS', 'ENRIN.NS', 'SIEMENS.NS', 'SIGNATURE.NS', 'SOBHA.NS', 'SOLARINDS.NS', 'SONACOMS.NS', 'SONATSOFTW.NS', 'STARHEALTH.NS', 'SBIN.NS', 'SAIL.NS', 'SUMICHEM.NS', 'SUNPHARMA.NS', 'SUNTV.NS', 'SUNDARMFIN.NS', 'SUPREMEIND.NS', 'SPLPETRO.NS', 'SUZLON.NS', 'SWANCORP.NS', 'SWIGGY.NS', 'SYNGENE.NS', 'SYRMA.NS', 'TBOTEK.NS', 'TVSMOTOR.NS', 'TATACAP.NS', 'TATACHEM.NS', 'TATACOMM.NS', 'TCS.NS', 'TATACONSUM.NS', 'TATAELXSI.NS', 'TATAINVEST.NS', 'TMCV.NS', 'TMPV.NS', 'TATAPOWER.NS', 'TATASTEEL.NS', 'TATATECH.NS', 'TTML.NS', 'TECHM.NS', 'TECHNOE.NS', 'TEGA.NS', 'TEJASNET.NS', 'TENNIND.NS', 'NIACL.NS', 'RAMCOCEM.NS', 'THERMAX.NS', 'TIMKEN.NS', 'TITAGARH.NS', 'TITAN.NS', 'TORNTPHARM.NS', 'TORNTPOWER.NS', 'TARIL.NS', 'TRAVELFOOD.NS', 'TRENT.NS', 'TRIDENT.NS', 'TRITURBINE.NS', 'TIINDIA.NS', 'UCOBANK.NS', 'UNOMINDA.NS', 'UPL.NS', 'UTIAMC.NS', 'ULTRACEMCO.NS', 'UNIONBANK.NS', 'UBL.NS', 'UNITDSPR.NS', 'URBANCO.NS', 'USHAMART.NS', 'VTL.NS', 'VBL.NS', 'VEDL.NS', 'VIJAYA.NS', 'VMM.NS', 'IDEA.NS', 'VOLTAS.NS', 'WAAREEENER.NS', 'WELCORP.NS', 'WELSPUNLIV.NS', 'WHIRLPOOL.NS', 'WIPRO.NS', 'WOCKPHARMA.NS', 'YESBANK.NS', 'ZFCVINDIA.NS', 'ZEEL.NS', 'ZENTEC.NS', 'ZENSARTECH.NS', 'ZYDUSLIFE.NS', 'ZYDUSWELL.NS', 'ECLERX.NS'
]

def scan_vcp_4only(ticker):
    try:
        df = yf.download(ticker, period='6mo', interval='1d', progress=False, auto_adjust=True)
        if df.empty or len(df) < 50: return None
        if isinstance(df.columns, pd.MultiIndex): df.columns = df.columns.droplevel(1)
        h, l, c, v = df['High'].squeeze(), df['Low'].squeeze(), df['Close'].squeeze(), df['Volume'].squeeze()
        df['range'] = h - l
        df['avg_range'] = df['range'].rolling(10).mean()
        contraction = df['avg_range'].iloc[-1] < df['avg_range'].iloc[-20:-10].mean()
        df['avg_vol'] = v.rolling(50).mean()
        vol_dry = v.iloc[-10:].mean() < df['avg_vol'].iloc[-1] * 0.7
        df['sma50'] = c.rolling(50).mean()
        above_sma = c.iloc[-1] > df['sma50'].iloc[-1]
        adx = ADXIndicator(high=h, low=l, close=c, window=14)
        strong_trend = adx.adx().iloc[-1] > 25
        rating = sum([contraction, vol_dry, above_sma, strong_trend])
        if rating == 4: # ONLY 4/4
            vcp_high = h.iloc[-20:].max()
            vcp_low = l.iloc[-20:].min()
            entry = round(vcp_high * 1.01, 2)
            sl = round(vcp_low * 0.99, 2)
            risk = entry - sl
            return {'Stock': ticker.replace('.NS',''), 'CMP': round(c.iloc[-1],2),
                    'Entry': entry, 'SL': sl, 'T1': round(entry + risk*2,2), 'T2': round(entry + risk*3,2)}
    except: return None

def scan_volume_surge(df, ticker):
    try:
        v, c = df['Volume'].squeeze(), df['Close'].squeeze()
        avg_vol_20 = v.rolling(20).mean() # CHANGED TO 20 DAYS
        if v.iloc[-1] > avg_vol_20.iloc[-1] * 3 and c.iloc[-1] > c.iloc[-2] * 1.02:
            entry = round(c.iloc[-1], 2)
            sl = round(c.iloc[-1] * 0.93, 2)
            risk = entry - sl
            return {'Stock': ticker.replace('.NS',''), 'Scan': 'VOL SURGE 3x20D', 'CMP': entry,
                    'Entry': entry, 'SL': sl, 'T1': round(entry + risk*2,2), 'T2': round(entry + risk*3,2)}
    except: return None

def scan_ath(df, ticker):
    try:
        h, c = df['High'].squeeze(), df['Close'].squeeze()
        ath = h.max()
        if c.iloc[-1] >= ath * 0.98:
            entry = round(ath * 1.01, 2)
            sl = round(ath * 0.95, 2)
            risk = entry - sl
            return {'Stock': ticker.replace('.NS',''), 'Scan': 'ATH B/O', 'CMP': round(c.iloc[-1],2),
                    'Entry': entry, 'SL': sl, 'T1': round(entry + risk*2.5,2), 'T2': round(entry + risk*4,2)}
    except: return None

def scan_cup_handle(df, ticker):
    try:
        c = df['Close'].squeeze()
        if len(c) < 120: return None
        cup_low_idx = c.iloc[-120:-20].idxmin()
        cup_low = c.loc[cup_low_idx]
        prior_high = c.iloc[-120:cup_low_idx].max()
        recovery_high = c.iloc[cup_low_idx:].max()
        drawdown = (prior_high - cup_low) / prior_high
        if 0.15 < drawdown < 0.4 and recovery_high >= prior_high * 0.95:
            handle_high = c.iloc[-20:].max()
            handle_low = c.iloc[-20:].min()
            handle_dd = (handle_high - handle_low) / handle_high
            if 0.05 < handle_dd < 0.15:
                entry = round(handle_high * 1.01, 2)
                sl = round(handle_low * 0.99, 2)
                risk = entry - sl
                return {'Stock': ticker.replace('.NS',''), 'Scan': 'CUP & HANDLE', 'CMP': round(c.iloc[-1],2),
                        'Entry': entry, 'SL': sl, 'T1': round(entry + risk*2,2), 'T2': round(entry + risk*3,2)}
    except: return None

def scan_pead(df, ticker):
    try:
        v, o, c = df['Volume'].squeeze(), df['Open'].squeeze(), df['Close'].squeeze()
        avg_vol = v.rolling(20).mean()
        for i in range(-5, 0):
            gap_up = o.iloc[i] > c.iloc[i-1] * 1.03
            vol_spike = v.iloc[i] > avg_vol.iloc[i] * 3
            if gap_up and vol_spike and c.iloc[-1] > o.iloc[i]:
                entry = round(c.iloc[-1], 2)
                sl = round(o.iloc[i] * 0.98, 2)
                risk = entry - sl
                return {'Stock': ticker.replace('.NS',''), 'Scan': 'PEAD', 'CMP': entry,
                        'Entry': entry, 'SL': sl, 'T1': round(entry + risk*2,2), 'T2': round(entry + risk*3,2)}
    except: return None

# Run all scanners
results = {'VCP 4/4': [], 'VOL SURGE 3x20D': [], 'ATH B/O': [], 'CUP & HANDLE': [], 'PEAD': []}
print("Scanning Nifty 500...")
for i, stock in enumerate(nifty500):
    if i % 50 == 0: print(f"Progress: {i}/500")
    try:
        df = yf.download(stock, period='1y', interval='1d', progress=False, auto_adjust=True)
        if df.empty or len(df) < 120: continue
        if isinstance(df.columns, pd.MultiIndex): df.columns = df.columns.droplevel(1)

        vcp_res = scan_vcp_4only(stock)
        if vcp_res: results['VCP 4/4'].append(vcp_res)

        for func, name in [(scan_volume_surge, 'VOL SURGE 3x20D'), (scan_ath, 'ATH B/O'),
                           (scan_cup_handle, 'CUP & HANDLE'), (scan_pead, 'PEAD')]:
            res = func(df, stock)
            if res: results[name].append(res)
    except: continue

# Build Email
sender = os.environ.get('GMAIL_USER')
password = os.environ.get('GMAIL_PASS')
receiver = os.environ.get('TO_EMAIL')

total_setups = sum(len(v) for v in results.values())
if total_setups == 0:
    subject = f"Elite Scan {datetime.now().strftime('%d-%b')}: No setups"
    body = "<p>No VCP 4/4, Volume Surge, ATH, Cup & Handle, or PEAD setups found today.</p>"
else:
    subject = f"Elite Scan {datetime.now().strftime('%d-%b')}: {total_setups} setups"
    body = f"<h2>Elite Nifty 500 Scan - {datetime.now().strftime('%d %b %Y')}</h2>"
    body += "<p><b>VCP 4/4 = Highest Priority.</b> Buy above Entry with vol > 1.5x 50-day avg. SL = pattern low.</p>"
    body += "<p><b>VOL SURGE = 3x 20-day avg volume</b> + 2% up close. For momentum trades.</p>"

    for scan_name, stocks in results.items():
        if stocks:
            df_scan = pd.DataFrame(stocks)
            body += f"<h3>{scan_name} - {len(stocks)} stocks</h3>"
            body += df_scan.to_html(index=False, border=1, justify='center')
            body += "<br>"

    body += "<p><i>Auto-generated at 9 PM IST. Not investment advice.</i></p>"

# Send Email
msg = MIMEMultipart()
msg['From'] = sender
msg['To'] = receiver
msg['Subject'] = subject
msg.attach(MIMEText(body, 'html'))

try:
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(sender, password)
    server.send_message(msg)
    server.quit()
    print(f"Email sent with {total_setups} setups")
except Exception as e:
    print(f"Email failed: {e}")
