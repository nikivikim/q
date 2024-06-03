from django.contrib.auth import authenticate, login
from django.views import View
from users.forms import UserCreationForm,  IndicatorValueForm
from django.shortcuts import render, get_object_or_404, redirect
from .forms import BalanceForm, IndicatorValueForm
import io
import base64
import urllib
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Balance, Indicator, IndicatorValue
import matplotlib.pyplot as plt
from datetime import timedelta
import calendar
from sklearn.linear_model import LinearRegression
import numpy as np
from sklearn.metrics import r2_score, mean_absolute_error, mean_squared_error
import numpy as np
import statsmodels.api as sm
@login_required
def edit_balance(request, balance_id):
    balance = get_object_or_404(Balance, id=balance_id, user=request.user)

    if request.method == 'POST':
        balance_form = BalanceForm(request.POST, instance=balance)
        if balance_form.is_valid():
            balance_form.save()

            # Обновляем данные индикаторов
            for indicator_value in balance.indicator_values.all():
                form_prefix = f'indicator_value_{indicator_value.id}'
                indicator_form = IndicatorValueForm(request.POST, instance=indicator_value, prefix=form_prefix)
                if indicator_form.is_valid():
                    indicator_form.save()

            # Перенаправляем на страницу отчета с использованием новых данных
            return report(request, balance_id=balance.id)

    else:
        balance_form = BalanceForm(instance=balance)
        indicator_forms = [
            IndicatorValueForm(instance=indicator_value, prefix=f'indicator_value_{indicator_value.id}')
            for indicator_value in balance.indicator_values.all()
        ]

    return render(request, 'edit_balance.html', {
        'balance_form': balance_form,
        'indicator_forms': indicator_forms,
        'balance': balance,
    })

@login_required
def create_balance(request):
    indicators = Indicator.objects.all()

    if request.method == 'POST':
        balance_form = BalanceForm(request.POST)
        indicator_forms = [IndicatorValueForm(request.POST, prefix=str(indicator.code)) for indicator in indicators]

        if balance_form.is_valid() and all(form.is_valid() for form in indicator_forms):
            balance = balance_form.save(commit=False)
            balance.user = request.user  # Присваиваем текущего пользователя
            balance.save()
            for form, indicator in zip(indicator_forms, indicators):
                indicator_value = form.save(commit=False)
                indicator_value.balance = balance
                indicator_value.indicator = indicator
                indicator_value.save()
            return redirect('report', balance_id=balance.id)  # Замените на ваш редирект
    else:
        balance_form = BalanceForm()
        indicator_forms = [IndicatorValueForm(prefix=str(indicator.code)) for indicator in indicators]

    indicator_form_data = zip(indicators, indicator_forms)

    return render(request, 'balance_form.html', {
        'balance_form': balance_form,
        'indicator_form_data': indicator_form_data,
    })

@login_required
def report(request, balance_id):
    balance = get_object_or_404(Balance, id=balance_id, user=request.user)
    indicator_values = balance.indicator_values.all()

    # Найдем значения необходимых индикаторов
    indicator_1200 = next((iv.value for iv in indicator_values if iv.indicator.code == '1200'), 0)
    indicator_1500 = next((iv.value for iv in indicator_values if iv.indicator.code == '1500'), 0)
    indicator_cash = next((iv.value for iv in indicator_values if iv.indicator.code == '1100'), 0)
    indicator_1700 = next((iv.value for iv in indicator_values if iv.indicator.code == '1700'), 0)
    indicator_1700_value2 = next((iv.value2 for iv in indicator_values if iv.indicator.code == '1700'), 0)
    indicator_1700_value3 = next((iv.value3 for iv in indicator_values if iv.indicator.code == '1700'), 0)

    indicator_quick_assets = next((iv.value for iv in indicator_values if iv.indicator.code == '1400'), 0)
    inventory = next((iv.value for iv in indicator_values if iv.indicator.code == '1300'), 0)
    leverage = round((indicator_quick_assets + indicator_1500) / inventory,2) if indicator_1500 != 0 else 0
    receivables = next((iv.value for iv in indicator_values if iv.indicator.code == '1400'),
                       0)  # Example for receivables
    active = next((iv.value for iv in indicator_values if iv.indicator.code == '1600'), 0)
    active_value2 = next((iv.value2 for iv in indicator_values if iv.indicator.code == '1600'), 0)
    active_value3 = next((iv.value3 for iv in indicator_values if iv.indicator.code == '1600'), 0)

    # Вычисляем коэффициенты ликвидности
    current_ratio = round(indicator_1200 / indicator_1500,2) if indicator_1500 != 0 else 0


    indicator_1240 = next((iv.value for iv in indicator_values if iv.indicator.code == '1240'), 0)
    indicator_1250 = next((iv.value for iv in indicator_values if iv.indicator.code == '1250'), 0)
    indicator_1230 = next((iv.value for iv in indicator_values if iv.indicator.code == '1230'), 0)

    indicator_1200_value2 = next((iv.value2 for iv in indicator_values if iv.indicator.code == '1200'), 0)
    indicator_1500_value2 = next((iv.value2 for iv in indicator_values if iv.indicator.code == '1500'), 0)
    indicator_cash_value2 = next((iv.value2 for iv in indicator_values if iv.indicator.code == '1100'), 0)
    indicator_1240_value2 = next((iv.value2 for iv in indicator_values if iv.indicator.code == '1240'), 0)
    indicator_1250_value2 = next((iv.value2 for iv in indicator_values if iv.indicator.code == '1250'), 0)
    indicator_1230_value2 = next((iv.value2 for iv in indicator_values if iv.indicator.code == '1230'), 0)

    indicator_1200_value3 = next((iv.value3 for iv in indicator_values if iv.indicator.code == '1200'), 0)
    indicator_1500_value3 = next((iv.value3 for iv in indicator_values if iv.indicator.code == '1500'), 0)
    indicator_cash_value3 = next((iv.value3 for iv in indicator_values if iv.indicator.code == '1100'), 0)
    indicator_1240_value3 = next((iv.value3 for iv in indicator_values if iv.indicator.code == '1240'), 0)
    indicator_1250_value3 = next((iv.value3 for iv in indicator_values if iv.indicator.code == '1250'), 0)
    indicator_1230_value3 = next((iv.value3 for iv in indicator_values if iv.indicator.code == '1230'), 0)
    indicator_1100_value3 = next((iv.value3 for iv in indicator_values if iv.indicator.code == '1100'), 0)
    indicator_1100 = next((iv.value for iv in indicator_values if iv.indicator.code == '1100'), 0)
    indicator_1100_value2 = next((iv.value2 for iv in indicator_values if iv.indicator.code == '1100'), 0)

    quick_ratio = round((indicator_1240 + indicator_1250+indicator_1230) / indicator_1500,2) if indicator_1500 != 0 else 0
    quick_ratio_value2 = round((indicator_1240_value2 + indicator_1250_value2+indicator_1230_value2) / indicator_1500_value2,2) if indicator_1500 != 0 else 0
    quick_ratio_value3 = round((indicator_1240_value3 + indicator_1250_value3+indicator_1230_value3) / indicator_1500_value3,2) if indicator_1500 != 0 else 0

    absolute_ratio = round(indicator_cash / indicator_1500,2) if indicator_1500 != 0 else 0
    autonomy_ratio = round(inventory / active,2)


    indicator_quick_assets_value2 = next((iv.value2 for iv in indicator_values if iv.indicator.code == '1400'), 0)
    total_assets_value2 = sum(iv.value2 for iv in indicator_values if iv.indicator.code.startswith('TA'))
    equity_value2 = sum(iv.value2 for iv in indicator_values if iv.indicator.code.startswith('EQ'))
    inventory_value2 = next((iv.value2 for iv in indicator_values if iv.indicator.code == '1300'), 0)  # Example for inventory
    receivables_value2 = next((iv.value2 for iv in indicator_values if iv.indicator.code == '1400'),
                       0)  # Example for receivables
    current_ratio_value2 = round(indicator_1200_value2 / indicator_1500_value2,2) if indicator_1500_value2 != 0 else 0
    absolute_ratio_value2 = round(indicator_cash_value2 / indicator_1500_value2,2) if indicator_1500_value2 != 0 else 0
    autonomy_ratio_value2 = round(inventory_value2 / active_value2,2)


    indicator_quick_assets_value3 = next((iv.value3 for iv in indicator_values if iv.indicator.code == '1400'), 0)
    total_assets_value3 = sum(iv.value3 for iv in indicator_values if iv.indicator.code.startswith('TA'))
    equity_value3 = sum(iv.value3 for iv in indicator_values if iv.indicator.code.startswith('EQ'))
    inventory_value3 = next((iv.value3 for iv in indicator_values if iv.indicator.code == '1300'), 0)  # Example for inventory

    receivables_value3 = next((iv.value3 for iv in indicator_values if iv.indicator.code == '1400'),
                       0)  # Example for receivables
    current_ratio_value3 = round(indicator_1200_value3 / indicator_1500_value3,2 ) if indicator_1500_value3 != 0 else 0
    absolute_ratio_value3 = round(indicator_cash_value3 / indicator_1500_value3,2) if indicator_1500_value3!= 0 else 0
    autonomy_ratio_value3 = round(inventory_value3 / active_value3,2)
    leverage_value2 = round((indicator_quick_assets_value2 + indicator_1500_value2) / inventory_value2,
                            2) if indicator_1500_value2 != 0 else 0
    leverage_value3 = round((indicator_quick_assets_value3 + indicator_1500_value3) / inventory_value3,
                            2) if indicator_1500_value3 != 0 else 0
    sos_value3 = round((inventory_value3 - indicator_1100_value3 ) / indicator_1200_value3,
                            2) if indicator_1200_value3 != 0 else 0
    sos_value2 = round((inventory_value2 - indicator_1100_value2 ) / indicator_1200_value2,
                            2) if indicator_1200_value2 != 0 else 0
    sos = round((inventory - indicator_1100 ) / indicator_1200,
                            2) if indicator_1200 != 0 else 0
    index_active = round(indicator_1100  / inventory,
                            2) if inventory != 0 else 0
    index_active_value2 = round(indicator_1100_value2 / inventory_value3,
                         2) if inventory_value3 != 0 else 0
    index_active_value3 = round(indicator_1100_value3 / inventory_value3,
                         2) if inventory_value3 != 0 else 0
    autonomy_ratio_change =round (autonomy_ratio - autonomy_ratio_value3, 2)
    leverage_change= round(leverage - leverage_value3, 2)
    sos_change = round(sos - sos_value3, 2)
    index_active_change = round(index_active - index_active_value3, 2)
    cm = round((inventory - indicator_1100)/inventory, 2) if inventory != 0 else 0
    cm_value2 = round((inventory_value2 - indicator_1100_value2) / inventory_value2, 2) if inventory_value2 != 0 else 0

    cm_value3 = round((inventory_value3 - indicator_1100_value2) / inventory_value3, 2) if inventory_value3 != 0 else 0
    cm_change = round((cm_value3 - cm),2)
    finance_stability = round((inventory+indicator_quick_assets)/ indicator_1700, 2) if indicator_1700 != 0 else 0
    finance_stability_value2 = round((inventory_value2 + indicator_quick_assets_value2) / indicator_1700_value2, 2) if indicator_1700_value2 != 0 else 0
    finance_stability_value3 = round((inventory_value3 + indicator_quick_assets_value3) / indicator_1700_value3, 2) if indicator_1700_value3 != 0 else 0
    finance_stability_change = round(finance_stability_value3-finance_stability, 2)
    # Генерация графика с помощью matplotlib
    fig, ax = plt.subplots(figsize=(10, 6))

    # Данные для гистограммы
    if calendar.isleap(balance.date.year - 1):
        days_to_subtract = 366
    else:
        days_to_subtract = 365

    # Получение новой даты на год меньше
    new_date = balance.date - timedelta(days=366)
    new_date2 = new_date - timedelta(days=days_to_subtract)
    # Создание графика
    # Создание графика
    plt.figure(figsize=(10, 6))

    # Построение графика для коэффициента ликвидности Value
    plt.plot([balance.date, new_date, new_date2], [current_ratio, current_ratio_value2, current_ratio_value3],
             label='Текущая ликвидность',)

    # Построение графика для коэффициента ликвидности Quick
    plt.plot([balance.date, new_date, new_date2], [quick_ratio, quick_ratio_value2, quick_ratio_value3], label='Быстрая ликвидность',
             color='red',)

    plt.plot([balance.date, new_date, new_date2], [absolute_ratio, absolute_ratio_value2, absolute_ratio_value3], label='Фбсолютная ликвидность',
             color='green',)

    plt.xlabel('Периоды')
    plt.ylabel('Значение коэффициента ликвидности')
    plt.title('Динамика коэффициентов ликвидности')
    plt.legend()
    plt.grid(True)
    plt.xticks([balance.date, new_date, new_date2], [balance.date, new_date, new_date2])

    # Преобразование графика в изображение PNG
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    string = base64.b64encode(buf.read())
    uri = urllib.parse.quote(string)



    analyse = []
    if current_ratio < 1.5:
        analyse.append("не соответсвует норме,")

    elif current_ratio > 2.5:
        analyse.append("превышает норму,")
    else:
        analyse.append("укладывается в норму,")

    if current_ratio < current_ratio_value2:
        decrease_percentage = (current_ratio_value2 - current_ratio)
        new_date = balance.date - timedelta(days=366)
        analyse.append(
            f"нужно обратить внимание на то, что по сравнению с {new_date.year} годом значение коэффициента снизилось на {decrease_percentage:.2f}.")
    elif current_ratio > current_ratio_value2:
        decrease_percentage = (current_ratio - current_ratio_value2  )
        new_date = balance.date - timedelta(days=366)
        analyse.append(
            f"нужно обратить внимание на то, что по сравнению с {new_date.year} годом значение коэффициента увеличилось на {decrease_percentage:.2f}.")
    analyse_absolute_ratio = []
    if absolute_ratio < absolute_ratio_value2:
        decrease_percentage_absolute = (absolute_ratio_value2 - absolute_ratio)
        analyse_absolute_ratio.append(
            f" снизился на {decrease_percentage_absolute} ")
    elif absolute_ratio > absolute_ratio_value2:
        decrease_percentage_absolute = round(absolute_ratio - absolute_ratio_value2, 2)
        analyse_absolute_ratio.append(
            f" увеличился на {decrease_percentage_absolute} ")


    analyse_quick_ratio = []
    if quick_ratio >= 0.7 and quick_ratio <= 0.7:
        decrease_percentage_quick_ratio = (quick_ratio_value2 - quick_ratio)
        analyse_quick_ratio.append(
            f" оказался в пределах нормы ({quick_ratio}). Это означает что у { balance.company_name } достаточно активов которые можно в сжатые сроки перевести в денежные средства, чтобы погасить краткосрочную кредиторскую задолженность.")
    elif quick_ratio > 1:
        decrease_percentage_quick_ratio = round(quick_ratio - quick_ratio_value2, 2)
        analyse_quick_ratio.append(
            f" превышает норму ({quick_ratio}). Это означает что у { balance.company_name } достаточно активов которые можно в сжатые сроки перевести в денежные средства, чтобы погасить краткосрочную кредиторскую задолженность. ")
    else:
        analyse_quick_ratio.append(
            f" ниже нормы ({quick_ratio}). Это означает что у {balance.company_name} недостаточно активов которые можно в сжатые сроки перевести в денежные средства, чтобы погасить краткосрочную кредиторскую задолженность. ")

    analyse_result = '\n'.join(analyse)
    analyse_result_analyse_absolute_ratio = '\n'.join(analyse_absolute_ratio)
    analyse_result_analyse_quick_ratio = '\n'.join(analyse_quick_ratio)

    # Пример данных о ликвидности за предыдущие годы

    years = np.array([new_date2.year, new_date.year, balance.date.year])

    liquidity = np.array([current_ratio_value2, current_ratio, current_ratio_value3])

    gdp = np.array([ 131.7458, 128.2497, 135.773])

    # Ожидаемое значение на следующий год

    inflation = np.array([ 3.0, 4.8, 8.39])  # Инфляция

    # Подготовка данных для модели
    X = sm.add_constant(np.column_stack((years, gdp, inflation)))  # Добавляем константу и макроэкономические показатели
    y = liquidity

    # Создаем и обучаем модель регрессии
    model = sm.OLS(y, X).fit()

    # Вывод результатов модели
    print(model.summary())

    # Прогнозируем значение ликвидности на следующий год
    next_year = 2025
    next_year_gdp = 134.080  # Предполагаемое значение ВВП на следующий год
    next_year_inflation = 11.9  # Предполагаемое значение инфляции на следующий год
    next_year_liquidity = model.predict([1, next_year, next_year_gdp, next_year_inflation])
    print(f"Прогноз коэффициента ликвидности на {next_year}: {next_year_liquidity[0]}")

    # Прогнозируемые значения
    predicted_values = model.predict(X)

    # Оценка точности с помощью метрик
    r2 = r2_score(y, predicted_values)
    mae = mean_absolute_error(y, predicted_values)
    mse = mean_squared_error(y, predicted_values)
    rmse = np.sqrt(mse)

    print(f"Коэффициент детерминации (R^2): {r2}")
    print(f"Средняя абсолютная ошибка (MAE): {mae}")
    print(f"Средняя квадратичная ошибка (MSE): {mse}")
    print(f"Корень из средней квадратичной ошибки (RMSE): {rmse}")

    total = indicator_1500 + receivables + inventory

    # Вычисляем процентные значения
    percentages = [
        indicator_1500 / total * 100,
        receivables / total * 100,
        inventory / total * 100
    ]
    capital_structure_labels = ['Собственный капитал', 'Краткосрочные обязательства', 'Долгосрочные обязательства']
    return render(request, 'report.html', {
        'balance': balance,
        'current_ratio_value2': current_ratio_value2,
        'quick_ratio_value2': quick_ratio_value2,
        'absolute_ratio_value2': absolute_ratio_value2,
        'chart1': string,  # Передача строки с изображением в шаблон
        'analyse_result':analyse_result,
        'analyse_result_analyse_absolute_ratio': analyse_result_analyse_absolute_ratio,
        'analyse_result_analyse_quick_ratio':analyse_result_analyse_quick_ratio,
        'sos': sos,
        'sos_value2': sos_value2,
        'sos_value3': sos_value3,
        'current_ratio_value3': current_ratio_value3,
        'quick_ratio_value3': quick_ratio_value3,
        'absolute_ratio_value3': absolute_ratio_value3,
        'total_capital':percentages,

        'leverage_change':leverage_change,
        'sos_change':sos_change,
        'index_active_change': index_active_change,
        'autonomy_ratio_change':autonomy_ratio_change,
        'capital_structure_labels': capital_structure_labels,
        'percentages':percentages,
        'finance_stability':finance_stability,
        'finance_stability_value2':finance_stability_value2,
        'finance_stability_value3':finance_stability_value3,
        'finance_stability_change':finance_stability_change,

        'previous_year_date': new_date,
        'previous_year_date2': new_date2,
        'index_active': index_active,
        'index_active_value2': index_active_value2,
        'index_active_value3':index_active_value3,
        'cm':cm,
        'cm_value2':cm_value2,
        'cm_value3':cm_value3,
        'cm_change':cm_change,
         'next_year_liquidity':next_year_liquidity,
         'leverage_value2':leverage_value2,
        'leverage': leverage,
        'leverage_value3': leverage_value3,
        'current_ratio': current_ratio,
        'quick_ratio': quick_ratio,
        'absolute_ratio': absolute_ratio,

        'autonomy_ratio': autonomy_ratio,
        'autonomy_ratio_value3': autonomy_ratio_value3,
        'autonomy_ratio_value2': autonomy_ratio_value2,
        'chart': uri,

        'indicator_1200': indicator_1200,
        'indicator_1500': indicator_1500,
        'indicator_cash': indicator_cash,
        'indicator_quick_assets': indicator_quick_assets,
        'inventory': inventory,
        'receivables': receivables,
    })

@login_required
def profile(request):
    balances = Balance.objects.filter(user=request.user).prefetch_related('indicator_values__indicator').order_by('-date')
    return render(request, 'profile.html', {'balances': balances})


class Register(View):
    template_name = 'registration/register.html'

    def get(self, request):
        context = {
            'form': UserCreationForm()
        }
        return render(request, self.template_name, context)

    def post(self, request):
        form = UserCreationForm(request.POST)

        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('home')
        context = {
            'form': form
        }
        return render(request, self.template_name, context)

