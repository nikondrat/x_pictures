import 'dart:developer';

import 'package:mobx/mobx.dart';
import 'package:x_pictures/src/data.dart';

part 'jobs.g.dart';

class JobsStore extends _JobsStore with _$JobsStore {
  JobsStore({required super.restClient});
}

abstract class _JobsStore with Store {
  final RestClient restClient;

  _JobsStore({required this.restClient});

  JobModel body = JobModel(
    id: 0,
    lora: LoraModel(
        id: '',
        status: Status.completed,
        estimatedTime: '',
        estimatedTimestamp: '',
        trainingTimeSeconds: 1,
        images: [],
        cost: '',
        createdDate: DateTime.now()),
    pack:
        PackModel(id: 1, title: '', description: '', category: '', images: []),
    images: [],
    timeSpent: 0,
    estimatedTime: 0,
    estimatedTimestamp: 0,
    status: Status.completed,
    cost: '',
    createdDate: DateTime.now(),
  );

  @observable
  ObservableFuture<List<JobModel>> fetchJobsFuture = emptyResponse;

  @observable
  ObservableList<JobModel> jobs = ObservableList();

  @action
  Future<List<JobModel>> fetchJobs() async {
    final future = restClient.get(Endpoint().jobs).then((v) {
      body = JobModel.fromJson(v!);

      log('$v');

      return body;
    });
    // fetchJobsFuture = ObservableFuture(future);
    // return jobs = ObservableList.of(await future);

    return [await future];
  }

  @computed
  bool get hasResults =>
      fetchJobsFuture != emptyResponse &&
      fetchJobsFuture.status == FutureStatus.fulfilled;

  static ObservableFuture<List<JobModel>> emptyResponse =
      ObservableFuture.value([]);
}
