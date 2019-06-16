#include<bits/stdc++.h>
#include<stdio.h>
#include<cmath>
#include<ctime>


using namespace std;

void swap(int* a, int* b)
{
    int t = *a;
    *a = *b;
    *b = t;
}

int * Mediana(int * a, int * b, int * c)
{
    if (*a < *b && * b < * c)
        return (b);
    if (*a < *c && *c <=* b)
        return (c);
    if (*b <= *a && *a < *c)
        return (a);
    if (*b < *c && * c <= * a)
        return (c);
    if (*c <= *a && *a < *b)
        return (a);
    if (*c <= *b && * b <= *a)
        return (b);
}

void merge(int * arr, int l, int m, int r)
{
    int i, j, k;
    int n1 = m - l + 1;
    int n2 =  r - m;

    int L[n1], R[n2];

    for (i = 0; i < n1; i++)
        L[i] = arr[l + i];
    for (j = 0; j < n2; j++)
        R[j] = arr[m + 1+ j];

    i = 0;
    j = 0;
    k = l;
    while (i < n1 && j < n2)
    {
        if (L[i] <= R[j])
        {
            arr[k] = L[i];
            i++;
        }
        else
        {
            arr[k] = R[j];
            j++;
        }
        k++;
    }


    while (i < n1)
    {
        arr[k] = L[i];
        i++;
        k++;
    }

    while (j < n2)
    {
        arr[k] = R[j];
        j++;
        k++;
    }
}
void quickSort(int *arr, int left, int right) {

      int i = left, j = right;
      int tmp;
      int pivot = arr[(left + right) / 2];

      while (i <= j) {

            while (arr[i] < pivot)
                  i++;

            while (arr[j] > pivot)
                  j--;

            if (i <= j) {
                  tmp = arr[i];
                  arr[i] = arr[j];
                  arr[j] = tmp;
                  i++;
                  j--;
            }
      };

      if (left < j)
            quickSort(arr, left, j);
      if (i < right)
            quickSort(arr, i, right);
}

void mergeSort(int * arr, int l, int r)
{
    if (l < r)
    {
        int m = (l+r)/2;

        mergeSort(arr, l, m);
        mergeSort(arr, m+1, r);
        merge(arr, l, m, r);
    }
}


int* Partition(int * arr , int low, int high)
{
    int pivot = arr[high];
    int i = (low - 1);

    for (int j = low; j <= high- 1; j++)
    {
        if (arr[j] <= pivot)
        {
            i++;
            swap(arr[i], arr[j]);
        }
    }
    swap(arr[i + 1], arr[high]);
    return (arr + i + 1);
}



void Introsort2(int * arr, int * begin,
                  int * end, int depth)
{
    // Count the number of elements
    int size = end - begin;

    if (depth == 0)
    {
        make_heap(begin, end+1);
        sort_heap(begin, end+1);
        return;
    }

    int * pivot = Mediana(begin, begin+size/2, end);

    swap(pivot, end);

    int * m = Partition(arr, begin-arr, end-arr);
    Introsort2(arr, begin, m-1, depth - 1);
    Introsort2(arr, m + 1, end, depth - 1);

    return;
}

void Introsort(int * arr, int *begin, int *end)
{
    int depthLimit = 2 * log(end-begin);

    Introsort2(arr, begin, end, depthLimit);

      return;
}

array<array<array<double,8>,5>,3> make_stats(){
    int number_of_arrays = 100;
    array<array<array<double,8>,5>,3> sorting_stats;
    int sizes[] = {10000, 50000, 100000, 500000, 1000000};
    int sizes_length = sizeof(sizes) / sizeof(sizes[0]);
    int percent_sorted[] = {0, 250, 500, 750, 950, 990, 997};
    int percent_sorted_length = sizeof(percent_sorted) / sizeof(percent_sorted[0]);

    for (int i=0; i < sizes_length; ++i){

        int test_array[sizes[i]];
        int test_array_length = sizeof(test_array) / sizeof(test_array[0]);
        for (int j=0; j < percent_sorted_length; ++j){

            double suma_q = 0;
            double suma_m = 0;
            double suma_i = 0;
            srand((unsigned)time(0));

            for(int k=0; k < number_of_arrays; ++k){

                for(int l=0; l < test_array_length; ++l){
                    int random1 = rand();
                    test_array[l] = random1;
                }

                if (percent_sorted[j] > 0) {
                    int not_sorted_start = floor(test_array_length * percent_sorted[j] / 1000);
                    sort(test_array, test_array + not_sorted_start);
                }

                int copy_test_array[sizes[i]];
                copy(test_array, test_array+test_array_length, copy_test_array);

                clock_t start = clock();
                quickSort(test_array, 0, test_array_length);
                clock_t end = clock();

                suma_q = suma_q + double(end - start) / CLOCKS_PER_SEC;

                copy(copy_test_array, copy_test_array+test_array_length, test_array);

                start = clock();
                mergeSort(test_array, 0, test_array_length)  ;

                end = clock();

                suma_m = suma_m + double(end - start) / CLOCKS_PER_SEC;

                copy(copy_test_array, copy_test_array+test_array_length, test_array);

                start = clock();
                Introsort(test_array, test_array, test_array + test_array_length - 1);
                end = clock();

                suma_i = suma_i + double(end - start) / CLOCKS_PER_SEC;

                cout << double(end - start);

            }
            sorting_stats[0][i][j] = suma_q /double(number_of_arrays);
            sorting_stats[1][i][j] = suma_m /double(number_of_arrays);
            sorting_stats[2][i][j] = suma_i /double(number_of_arrays);

            suma_q = 0;
            suma_m = 0;
            suma_i = 0;

        for(int k=0; k < number_of_arrays; ++k){
            srand((unsigned)time(0));
            for(int l=0; l < test_array_length; ++l){
                int random = (rand() % 10000) - 500;
                test_array[l] = random;
            }
            sort(test_array, test_array + test_array_length, greater<int>());
            int copy_test_array[sizes[i]];
            copy(test_array, test_array+test_array_length, copy_test_array);

            clock_t start = clock();
            quickSort(test_array, 0, test_array_length);
            clock_t end = clock();

            suma_q = suma_q + double(end - start) / CLOCKS_PER_SEC;

            copy(copy_test_array, copy_test_array+test_array_length, test_array);

            start = clock();
            mergeSort(test_array, 0, test_array_length)  ;
            end = clock();

            suma_m = suma_m + double(end - start) / CLOCKS_PER_SEC;

            copy(copy_test_array, copy_test_array+test_array_length, test_array);

            start = clock();
            Introsort(test_array, test_array, test_array + test_array_length - 1);
            end = clock();

            suma_i = suma_i + double(end - start) / CLOCKS_PER_SEC;

            }
            sorting_stats[0][i][7] = suma_q /double(number_of_arrays);
            sorting_stats[1][i][7] = suma_m /double(number_of_arrays);
            sorting_stats[2][i][7] = suma_i /double(number_of_arrays);
        }
    }
    return sorting_stats;
}

int main()
{
    array<array<array<double,8>,5>,3> stats = make_stats();
    ofstream myfile;
    myfile.open ("example.csv");

    cout << "Quick" << endl << endl;
    for(int i=0 ; i < 5 ; ++i)
    {
        for(int j= 0 ; j< 8; ++j){
            myfile << setprecision(10)<< stats[0][i][j] << ",";
        }
        myfile << endl;
    }
    myfile << endl;
    cout << "Merge" << endl << endl;
    for(int i=0 ; i < 5 ; ++i)
    {
        for(int j= 0 ; j< 8; ++j){
            myfile << setprecision(10)<< stats[1][i][j] << ",";
        }
        myfile << endl;
    }
    myfile << endl;
    cout << "Intro" << endl << endl;
    for(int i=0 ; i < 5 ; ++i)
    {
        for(int j= 0 ; j< 8; ++j){
            myfile << setprecision(10)<< stats[2][i][j] << ",";
        }
        myfile << endl;

    }
    myfile.close();

    return 0;
}
